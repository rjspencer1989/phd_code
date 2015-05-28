import couchdb_config_parser
import datetime
db = couchdb_config_parser.get_db()


def add_history_item(title, description, user, docId, docRev, undoable):
    doc = {}
    doc['collection'] = 'events'
    doc['title'] = title
    doc['description'] = description
    doc['user'] = user
    doc['timestamp'] = datetime.datetime.now().isoformat()
    doc['doc_id'] = docId
    doc['doc_rev'] = docRev
    doc['undoable'] = undoable
    doc['perform_undo'] = False
    res = db.save_doc(doc)
    return res
