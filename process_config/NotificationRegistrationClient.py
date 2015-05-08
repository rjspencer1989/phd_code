#!/usr/bin/python

import urllib
import urllib2

from couchdbkit import *
from Queue import Queue
import threading
import CouchdbConfigParser
db = CouchdbConfigParser.getDB()
db_info = db.info()


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
            print theId
            currentDoc = db.open_doc(theId, rev=theRev)
            if theRev.startswith('1-'):
                self.registration(currentDoc)
            elif '_deleted' in currentDoc:
                self.delete(currentDoc)
            else:
                self.edit(currentDoc)
            self.shared_object.task_done()

    def get_router_id(self):
        router = ''
        with open('/etc/homework/notification.conf') as f:
            router = f.read()

        routerArr = router.split('=')
        if len(routerArr) == 2:
            router = routerArr[1].strip()
        return router

    def edit(self, doc):
        data = urllib.urlencode({'service': doc['service'], 'userdetails': doc['user'], 'suid': doc['suid']})
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        router = self.get_router_id()
        if len(router) > 0:
            try:
                req = urllib2.Request("https://2-dot-homework-notify.appspot.com/notify/2/%s/register" % (router), data, headers)
                conn = urllib2.urlopen(req)
                code = conn.getcode()
                if code == 200:
                    response = conn.read()
                    print response
                    doc['suid'] = response
                    db.save_doc(doc)
            except urllib2.HTTPError, e:
                print e.code
                print e.read()
            except urllib2.URLError, e:
                print e.reason

    def delete(self, doc):
        data = urllib.urlencode({'suid': doc['suid']})
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        router = self.get_router_id()
        if len(router) > 0:
            try:
                req = urllib2.Request("https://2-dot-homework-notify.appspot.com/notify/2/%s/register" % (router), data, headers)
                conn = urllib2.urlopen(req)
                conn.getcode()
            except urllib2.HTTPError, e:
                print e.code
                print e.read()
            except urllib2.URLError, e:
                print e.reason

    def registration(self, doc):
        data = urllib.urlencode({'service': doc['service'], 'userdetails': doc['user']})
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        router = self.get_router_id()
        if len(router) > 0:
            try:
                req = urllib2.Request("https://2-dot-homework-notify.appspot.com/notify/2/%s/register" % (router), data, headers)
                conn = urllib2.urlopen(req)
                code = conn.getcode()
                if code == 200:
                    response = conn.read()
                    print response
                    doc['suid'] = response
                    db.save_doc(doc)
            except urllib2.HTTPError, e:
                print e.code
                print e.read()
            except urllib2.URLError, e:
                print e.reason

changeQueue = Queue()
producer = NotificationListener("producer", changeQueue)
consumer = NotificationProcessor("consumer", changeQueue)
producer.start()
consumer.start()
