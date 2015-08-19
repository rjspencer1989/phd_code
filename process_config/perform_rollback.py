from add_history import add_history_item
import undo
import datetime
from dateutil.tz import tzlocal
import dateutil.parser


class Rollback(object):
    def __init__(self, db, change):
        self.db = db
        self.change = change

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
        result = True
        doc_list = self.get_docs_to_revert(timestamp)
        for key, doc in doc_list.iteritems():
            doc['perform_undo'] = True
            res = self.db.save_doc(doc)
            if 'ok' not in res:
                result = False
        return result

    def rollback(self):
        if 'id' in self.change:
            the_id = self.change['id']
            the_rev = self.change['changes'][0]['rev']
            current_doc = self.db.get(the_id, rev=the_rev)

            self.revert(current_doc['timestamp'])
            dt = dateutil.parser.parse(current_doc['timestamp'])
            dt = dt.astimezone(tzlocal())
            add_history_item("Rollback", "Roll back to %s" % (dt.isoformat(' ')),
                             the_id, the_rev, 'request_revert', undoable=True)
            current_doc['status'] = 'done'
            res = self.db.save_doc(current_doc, force_update=True)
            return res
