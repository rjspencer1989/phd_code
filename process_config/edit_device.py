#!/usr/bin/env python

from add_history import add_history_item


def edit_device(current_doc):
    title = 'Edited device details'
    desc = 'Edited details for %s' % (current_doc['device_name'])
    add_history_item(title, desc, theId, theRev, True, ts=current_doc['event_timestamp'])
