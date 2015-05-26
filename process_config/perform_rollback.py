import couchdb_config_parser
from couchdbkit import *
from Queue import Queue
import threading
import os


class RollbackListener(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.db = couchdb_config_parser.get_db()
        self.db_info = self.db.info()
        self.shared_object = queue

    def run(self):
        change_stream = ChangesStream(db, feed='continuous', heartbeat=True, since=self.db_info['update_seq'], filter='homework-remote/rollback')
        for change in change_stream:
            self.shared_object.put(change)


class RollbackProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.events = None
        self.shared_object = queue
        self.db = couchdb_config_parser.get_db()

    def get_events_after_timestamp(self):
        vr = self.db.view('homework-remote/events', startkey=self.timestamp)
        self.events = vr.all()
        return self.events

    def get_docs_to_revert(self):
        self.get_events_after_timestamp()
        doc_list = {}
        for event_val in self.events:
            event = event_val['value']
            if event['doc_id'] not in doc_list:
                doc_list[event['doc_id']] = event
        return doc_list

    def run(self):
        while True:
            change = self.shared_object.get()
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            current_doc = self.db.get(the_id, rev=the_rev)
            self.shared_object.task_done()
change_queue = Queue()
producer = RollbackListener('producer', change_queue)
consumer = RollbackProcessor('consumer', change_queue)
if 'ENV_TESTS' not in os.environ:
    producer.start()
    consumer.start()
