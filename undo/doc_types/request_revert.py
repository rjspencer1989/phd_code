from base_doc import BaseDoc
from process_config import perform_rollback


class Request_revert(BaseDoc):
    def get_rev_list(self):
        return []

    def get_events(self, ts):
        vr = self.db.view('homework-remote/undoable_events', startkey=ts)
        return vr

    def undo(self):
        rev_list = self.get_rev_list()
        ts = self.doc['timestamp']
        events = self.get_events(ts).all()

    def get_reverted_events(self):
        return None
