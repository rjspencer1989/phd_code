#!/usr/bin/env python

from couchdbkit import *
from Queue import Queue
import threading
import couchdb_config_parser
import os
import set_dns

db = couchdb_config_parser.get_db()
db_info = db.info()


class SetDNSListener(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        changeStream = ChangesStream(db, feed="continuous", heartbeat=True, since=db_info['update_seq'], filter='homework-remote/dns_set')
        for change in changeStream:
            self.shared_object.put(change)


class SetDNSProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        while True:
            change = self.shared_object.get()
            if 'id' in change and change['id'] == 'dns':
                theRev = change['changes'][0]['rev']
                current_doc = db.get('dns', rev=theRev)
                set_dns.set_dns(current_doc)
            self.shared_object.task_done()

changeQueue = Queue()
producer = SetDNSListener("producer", changeQueue)
consumer = SetDNSProcessor("consumer", changeQueue)

producer.start()
consumer.start()
