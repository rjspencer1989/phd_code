import couchdb_config_parser
from couchdbkit import *


class Rollback(object):
    def __init__(self, timestamp):
        self.db = couchdb_config_parser.get_db()
        self.events = None
        self.timestamp = timestamp

    def get_events_after_timestamp(self):
        vr = self.db.view('homework-remote/events', descending=True, endkey=self.timestamp)
        vra = vr.all()
        return vra

    def perform_rollback(self):
        self.events = self.get_events_after_timestamp()
