import CouchdbConfigParser
import datetime
db = CouchdbConfigParser.getDB()


def addHistoryItem(title, description, user, docId, docRev, undoable):
    doc = {}
    doc['collection'] = 'events'
    doc['title'] = title
    doc['description'] = description
    doc['user'] = user
    doc['timestamp'] = datetime.datetime.now().isoformat()
    doc['doc_id'] = docId
    doc['doc_rev'] = docRev
    doc['undoable'] = undoable
    doc['process_undo'] = False
    res = db.save_doc(doc)
    return res
