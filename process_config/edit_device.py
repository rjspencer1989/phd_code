#!/usr/bin/env python

from add_history import add_history_item
import couchdb_config_parser

db = couchdb_config_parser.get_db()


def edit_device(current_doc):
    title = 'Edited device details'
    desc = 'Edited details for %s' % (current_doc['device_name'])
    add_history_item(title, desc, theId, theRev, True, ts=current_doc['event_timestamp'])
    if 'event_timestamp' in current_doc:
        del current_doc['event_timestamp']
        db.save_doc(current_doc, force_update=True)
