#!/usr/bin/env python

from couchdbkit import *
from Queue import Queue
import threading
import couchdb_config_parser
import os
import edit_main_user

db = couchdb_config_parser.get_db()
db_info = db.info()


class EditUserListener(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        changeStream = ChangesStream(db, feed="continuous", heartbeat=True, since=db_info['update_seq'], filter='homework-remote/main_user')
        for change in changeStream:
            self.shared_object.put(change)


class EditUserProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        while True:
            change = self.shared_object.get()
            if 'id' in change and change['id'] == 'main_user':
                theRev = change['changes'][0]['rev']
                current_doc = db.get('main_user', rev=theRev)
                edit_main_user.edit_user(current_doc)
            self.shared_object.task_done()

changeQueue = Queue()
producer = EditUserListener("producer", changeQueue)
consumer = EditUserProcessor("consumer", changeQueue)

producer.start()
consumer.start()
