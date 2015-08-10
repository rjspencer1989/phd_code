#!/usr/bin/env python

from process_config import couchdb_config_parser
import perform_undo
from couchdbkit import *
from Queue import Queue
import threading
import os
db = couchdb_config_parser.get_db()
db_info = db.info()

class UndoListener(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        changeStream = ChangesStream(db, feed="continuous", heartbeat=True, since=db_info['update_seq'], filter="homework-remote/undo")
        for change in changeStream:
            self.shared_object.put(change)


class UndoProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        while(True):
            change = self.shared_object.get()
            if 'id' in change:
                the_id = change['id']
                the_rev = change['changes'][0]['rev']
                current_doc = db.open_doc(the_id, rev=the_rev)
                perform_undo.perform_undo(current_doc)
            self.shared_object.task_done()

changeQueue = Queue()
producer = UndoListener("producer", changeQueue)
consumer = UndoProcessor("consumer", changeQueue)
producer.start()
consumer.start()
