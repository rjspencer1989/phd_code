#!/usr/bin/env python

from process_config import couchdb_config_parser
from couchdbkit import *
from Queue import Queue
import threading
import os
from process_config import add_history
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

    def get_doc_to_undo(self, event):
        undo_id = event['doc_id']
        undo_doc = db.get(undo_id, revs_info=True)
        return undo_doc

    def perform_undo(self, event):
        doc = self.get_doc_to_undo(event)
        import_name = 'undo.doc_types.%s' % (doc['collection'])
        mod = __import__(import_name, fromlist=[''])
        result = mod.undo(doc)

    def run(self):
        while(True):
            change = self.shared_object.get()
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            current_doc = db.open_doc(the_id, rev=the_rev)
            self.perform_undo(current_doc)
            self.shared_object.task_done()

changeQueue = Queue()
producer = UndoListener("producer", changeQueue)
consumer = UndoProcessor("consumer", changeQueue)
if "ENV_TESTS" not in os.environ:
    producer.start()
    consumer.start()
