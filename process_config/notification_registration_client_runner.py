#!/usr/bin/python

import os

from couchdbkit import *
from Queue import Queue
from pprint import pprint
import threading
import couchdb_config_parser
import add_history
import notification_registration_client

db = couchdb_config_parser.get_db()
db_info = db.info()
pprint(db_info)


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
            print change
            theId = change['id']
            theRev = change['changes'][0]['rev']
            currentDoc = db.open_doc(theId, rev=theRev)
            if theRev.startswith('1-'):
                notification_registration_client.registration(currentDoc)
            elif 'hidden' in currentDoc:
                notification_registration_client.delete(currentDoc)
            else:
                notification_registration_client.edit(currentDoc)
            self.shared_object.task_done()

changeQueue = Queue()
producer = NotificationListener("producer", changeQueue)
consumer = NotificationProcessor("consumer", changeQueue)

if "ENV_TESTS" not in os.environ:
    producer.start()
    consumer.start()
