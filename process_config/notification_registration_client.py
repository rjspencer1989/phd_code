#!/usr/bin/python

import urllib
import urllib2
import os

from couchdbkit import *
from Queue import Queue
import threading
import couchdb_config_parser
db = couchdb_config_parser.get_db()
db_info = db.info()


def get_router_id():
    return os.environ['APP_ENGINE_ROUTER_ID']


class NotificationListener(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        changeStream = ChangesStream(db, feed="continuous", heartbeat=True, since=db_info['update_seq'], filter="homework-remote/notifications")
        for change in changeStream:
            self.shared_object.put(change)


class NotificationProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        while(True):
            change = self.shared_object.get()
            theId = change['id']
            theRev = change['changes'][0]['rev']
            currentDoc = db.open_doc(theId, rev=theRev)
            if theRev.startswith('1-'):
                self.registration(currentDoc, router_id)
            elif '_deleted' in currentDoc:
                self.delete(currentDoc, router_id)
            else:
                self.edit(currentDoc, router_id)
            self.shared_object.task_done()

    def edit(self, doc, router):
        data = urllib.urlencode({'service': doc['service'], 'userdetails': doc['user'], 'suid': doc['suid']})
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        if len(router) > 0:
            try:
                req = urllib2.Request("https://2-dot-homework-notify.appspot.com/notify/2/%s/edit" % (router), data, headers)
                conn = urllib2.urlopen(req)
                code = conn.getcode()
                if code == 200:
                    response = conn.read()
                    doc['suid'] = response
                    doc['status'] = 'done'
            except urllib2.HTTPError, e:
                doc['status'] = 'error'
            except urllib2.URLError, e:
                doc['status'] = 'error'
            finally:
                db.save_doc(doc)

    def delete(self, doc, router):
        data = urllib.urlencode({'suid': doc['suid']})
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        if len(router) > 0:
            try:
                req = urllib2.Request("https://2-dot-homework-notify.appspot.com/notify/2/%s/delete" % (router), data, headers)
                conn = urllib2.urlopen(req)
                code = conn.getcode()
                return code
            except urllib2.HTTPError, e:
                return e.code
            except urllib2.URLError, e:
                return -1

    def registration(self, doc, router):
        data = urllib.urlencode({'service': doc['service'], 'userdetails': doc['user']})
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        if len(router) > 0:
            try:
                req = urllib2.Request("https://2-dot-homework-notify.appspot.com/notify/2/%s/register" % (router), data, headers)
                conn = urllib2.urlopen(req)
                code = conn.getcode()
                if code == 200:
                    response = conn.read()
                    doc['suid'] = response
                    doc['status'] = 'done'
            except urllib2.HTTPError, e:
                doc['status'] = 'error'
            except urllib2.URLError, e:
                doc['status'] = 'error'
            finally:
                db.save_doc(doc)

router_id = get_router_id()
changeQueue = Queue()
producer = NotificationListener("producer", changeQueue)
consumer = NotificationProcessor("consumer", changeQueue)

if "ENV_TESTS" not in os.environ:
    producer.start()
    consumer.start()
