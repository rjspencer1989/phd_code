#!/usr/bin/env python

from couchdbkit import *
from Queue import Queue
import threading
import couchdb_config_parser
import add_history
import os

db = couchdb_config_parser.get_db()
db_info = db.info()


class EditDeviceListener(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        changeStream = ChangesStream(db, feed="continuous", heartbeat=True, since=db_info['update_seq'], filter='homework-remote/edit_device')
        for change in changeStream:
            print change
            self.shared_object.put(change)


class EditDeviceProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        while True:
            change = self.shared_object.get()
            theId = change['id']
            theRev = change['changes'][0]['rev']
            current_doc = db.get(theId, rev=theRev)
            print current_doc
            add_history.add_history_item('Edited device details', 'Edited details for %s' % (current_doc['device_name']), theId, theRev, True)
            self.shared_object.task_done()

changeQueue = Queue()
producer = EditDeviceListener("producer", changeQueue)
consumer = EditDeviceProcessor("consumer", changeQueue)

if "ENV_TESTS" not in os.environ:
    producer.start()
    consumer.start()
