import couchdb_config_parser
from couchdbkit import *
import pprint


class Rollback(object):
    def __init__(self, timestamp):
        self.db = couchdb_config_parser.get_db()
        self.events = None
        self.timestamp = timestamp

    def get_events_after_timestamp(self):
        vr = self.db.view('homework-remote/events', startkey=self.timestamp)
        self.events = vr.all()
        return self.events

    def get_docs_to_revert(self):
        self.get_events_after_timestamp()
        pprint.pprint(self.events)
        doc_list = {}
        for event_val in self.events:
            event = event_val['value']
            doc_list[event['doc_id']] = event
        return doc_list
