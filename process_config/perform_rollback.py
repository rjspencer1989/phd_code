from add_history import add_history_item
from undo import perform_undo
import datetime
from dateutil.tz import tzlocal
from collections import OrderedDict
import dateutil.parser
import pprint


class Rollback(object):
    def __init__(self, db, change):
        self.db = db
        self.change = change

    def get_events_after_timestamp(self, ts):
        vr = self.db.view('homework-remote/undoable_events', startkey=ts)
        return vr.all()

    def get_docs_to_revert(self, timestamp):
        events = self.get_events_after_timestamp(timestamp)
        doc_list = OrderedDict()
        for event_val in events:
            event = event_val['value']
            for ed_doc in event['docs']:
                if ed_doc['doc_id'] not in doc_list:
                    doc_list[ed_doc['doc_id']] = event
        pprint.pprint(doc_list)
        return doc_list

    def revert(self, timestamp):
        doc_arr = []
        doc_list = self.get_docs_to_revert(timestamp)
        for key, doc in reversed(doc_list.items()):
            print "%s - %s\n" % (key, doc['_id'])
            r = perform_undo.perform_undo(doc)
            item = {}
            item['doc_id'] = key
            item['doc_rev'] = r
            item['doc_collection'] = doc['collection']
            item['action'] = 'edit'
            doc_arr.append(item)
        return doc_arr

    def rollback(self):
        if 'id' in self.change:
            the_id = self.change['id']
            the_rev = self.change['changes'][0]['rev']
            current_doc = self.db.get(the_id, rev=the_rev)

            r = self.revert(current_doc['timestamp'])
            dt = dateutil.parser.parse(current_doc['timestamp'])
            dt = dt.astimezone(tzlocal())
            add_history_item("Rollback", "Roll back to %s" % (dt.isoformat(' ')),
                             r, undoable=True)
            current_doc['status'] = 'done'
            res = self.db.save_doc(current_doc, force_update=True)
            return res
