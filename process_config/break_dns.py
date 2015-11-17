#!/usr/bin/env python

from add_history import add_history_item
import couchdb_config_parser

db = couchdb_config_parser.get_db()


def break_dns(current_doc):
    title = 'DNS settings updated'
    desc = 'You are now using Google\'s DNS servers.
    ts = current_doc['event_timestamp'] if 'event_timestamp' in current_doc else None
    add_history_item(title, desc, current_doc['_id'], current_doc['_rev'], 'main_user', 'edit', True, ts=ts)
    if 'event_timestamp' in current_doc:
        del current_doc['event_timestamp']
        db.save_doc(current_doc, force_update=True)
