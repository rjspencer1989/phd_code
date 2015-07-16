#!/usr/bin/env python

import couchdb_config_parser
from couchdbkit import *
from Queue import Queue
import threading
import os
from add_history import add_history_item


class RollbackListener(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.db = couchdb_config_parser.get_db()
        self.db_info = self.db.info()
        self.shared_object = queue

    def run(self):
        change_stream = ChangesStream(self.db,
                                      feed='continuous',
                                      heartbeat=True,
                                      since=self.db_info['update_seq'],
                                      filter='homework-remote/revert')
        for change in change_stream:
            self.shared_object.put(change)


class RollbackProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue
        self.db = couchdb_config_parser.get_db()

    def get_events_after_timestamp(self, ts):
        vr = self.db.view('homework-remote/undoable_events', startkey=ts)
        return vr.all()

    def get_docs_to_revert(self, timestamp):
        events = self.get_events_after_timestamp(timestamp)
        doc_list = {}
        for event_val in events:
            event = event_val['value']
            if event['doc_id'] not in doc_list:
                doc_list[event['doc_id']] = event
        return doc_list

    def revert(self, timestamp):
        doc_list = self.get_docs_to_revert(timestamp)
        for key, doc in doc_list.iteritems():
            doc['perform_undo'] = True
            self.db.save_doc(doc)

    def run(self):
        while True:
            change = self.shared_object.get()
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            current_doc = self.db.get(the_id, rev=the_rev)
            self.revert(current_doc['timestamp'])
            add_history_item("Rollback", "Roll back to %s" % (timestamp),
                             the_id, the_rev, False)
            doc.status = 'done'
            db.save_doc(current_doc['_id'])
            self.shared_object.task_done()
change_queue = Queue()
producer = RollbackListener('producer', change_queue)
consumer = RollbackProcessor('consumer', change_queue)

if 'ENV_TESTS' not in os.environ:
    producer.start()
    consumer.start()
