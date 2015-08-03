#!/usr/bin/env python

from couchdbkit import *
from Queue import Queue
import threading
from datetime import datetime
import couchdb_config_parser
import subprocess
import change_notification
import os
import add_history
import pprint
import edit_wifi

db = couchdb_config_parser.get_db()
db_info = db.info()


class WifiListener(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue
        self.since = db_info['update_seq']

    def run(self):
        changeStream = ChangesStream(db, feed="continuous", heartbeat=True, since=self.since, filter="homework-remote/wifi")
        for change in changeStream:
            self.shared_object.put(change)
            pprint.pprint(change)


class WifiProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue
        self.devices = None

    def run(self):
        while(True):
            change = self.shared_object.get()
            if 'id' in change:
                the_id = change['id']
                the_rev = change['changes'][0]['rev']
                current_doc = db.open_doc(the_id, rev=the_rev)
                edit_wifi.process_wifi(current_doc)
            self.shared_object.task_done()

changeQueue = Queue()
producer = WifiListener("producer", changeQueue)
consumer = WifiProcessor("consumer", changeQueue)
if 'ENV_TESTS' not in os.environ:
    producer.start()
    consumer.start()
