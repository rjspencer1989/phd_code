#!/usr/bin/env python

import couchdb_config_parser
from couchdbkit import *
from Queue import Queue
import threading
import os
import add_history
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

changeQueue = Queue()
producer = UndoListener("producer", changeQueue)
consumer = UndoProcessor("consumer", changeQueue)
if "ENV_TESTS" not in os.environ:
    producer.start()
    consumer.start()
