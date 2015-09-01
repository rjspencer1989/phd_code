#!/usr/bin/env python

from add_history import add_history_item
import couchdb_config_parser

db = couchdb_config_parser.get_db()


def edit_user(current_doc, from_undo=False):
    title = 'Edited main user'
    desc = 'Main user is %s, receiving notifications via %s' % (current_doc['name'], current_doc['service'])
    if from_undo is True:
        title = 'Undo Edit Main User'
        desc = 'Undo Edit of Main User. %s' % (desc)
    ts = current_doc['event_timestamp'] if 'event_timestamp' in current_doc else None
    add_history_item(title, desc, current_doc['_id'], current_doc['_rev'], 'main_user', 'edit', True, ts=ts)
    if 'event_timestamp' in current_doc:
        del current_doc['event_timestamp']
        current_doc['status'] = 'done'
        db.save_doc(current_doc, force_update=True)
