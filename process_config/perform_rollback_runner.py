#!/usr/bin/env python

import couchdb_config_parser
from couchdbkit import *
from Queue import Queue
import threading
import os
from perform_rollback import Rollback


class RollbackListener(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.db = couchdb_config_parser.get_db()
        self.db_info = self.db.info()
        self.shared_object = queue

    def run(self):
        change_stream = ChangesStream(self.db, feed='continuous', heartbeat=True, since=self.db_info['update_seq'], filter='homework-remote/revert')
        for change in change_stream:
            self.shared_object.put(change)


class RollbackProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue
        self.db = couchdb_config_parser.get_db()

    def run(self):
        while True:
            change = self.shared_object.get()
            roller = Rollback(self.db, change)
            roller.rollback()
            self.shared_object.task_done()
change_queue = Queue()
producer = RollbackListener('producer', change_queue)
consumer = RollbackProcessor('consumer', change_queue)

if 'ENV_TESTS' not in os.environ:
    producer.start()
    consumer.start()
