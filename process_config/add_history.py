import couchdb_config_parser
import datetime
from dateutil.tz import tzutc
db = couchdb_config_parser.get_db()


def add_history_item(title, description, docId, docRev, doc_collection, action='edit', undoable, ts=None):
    doc = {}
    doc['collection'] = 'events'
    doc['title'] = title
    doc['description'] = description
    doc['doc_collection'] = doc_collection
    doc['action'] = action
    if ts is None:
        doc['timestamp'] = datetime.datetime.now(tzutc()).isoformat()
    else:
        doc['timestamp'] = ts
    doc['doc_id'] = docId
    doc['doc_rev'] = docRev
    doc['undoable'] = undoable
    doc['perform_undo'] = False
    res = db.save_doc(doc)
    return res
