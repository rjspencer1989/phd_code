#!/usr/bin/env python

from process_config import add_history, couchdb_config_parser
db = couchdb_config_parser.get_db()

def get_doc_to_undo(event):
    if len(event[docs]) == 1:
        undo_id = event['doc_id']
        undo_doc = db.get(undo_id, revs_info=True)
        return undo_doc

def perform_undo(event):
    doc = get_doc_to_undo(event)
    import_name = 'undo.doc_types.%s' % (doc['collection'])
    class_name = doc['collection'].capitalize()
    mod = __import__(import_name, fromlist=[''])
    instance = getattr(mod, class_name)(doc, event)
    result = instance.undo()
    return result
