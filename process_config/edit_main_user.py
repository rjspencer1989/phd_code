#!/usr/bin/env python

from add_history import add_history_item


def edit_user(current_doc):
    title = 'Edited main user'
    desc = 'Main user is %s, receiving notifications via %s' % (current_doc['name'], current_doc['service'])
    add_history_item(title, desc, current_doc['_id'], current_doc['_rev'], True, ts=current_doc['event_timestamp'])
