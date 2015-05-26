import couchdb_config_parser
from couchdbkit import *


class Rollback(object):
    def __init__(self, timestamp):
        self.db = couchdb_config_parser.get_db()
        self.events = None
        self.timestamp = timestamp

    def get_events_after_timestamp(self):
        vr = self.db.view('homework-remote/events', descending=True, endkey=self.timestamp)
        self.events = vr.all()
        return self.events

    def get_doc_for_event(self, event):
        doc = self.db.get(event['doc_id'], rev=event['doc_rev'])
        return doc

    def get_docs_to_revert(self):
        self.get_events_after_timestamp()
        doc_list = []
        for event in self.events:
            doc_list.append(self.get_doc_for_event(event))
        return doc_list
