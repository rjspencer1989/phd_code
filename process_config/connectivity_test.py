#!/usr/bin/python
import urllib2
from add_history import add_history_item
import couchdb_config_parser

db = couchdb_config_parser.get_db()
doc = db.get('connection_state')
req = urllib2.Request('http://rjspencer1989.koding.io')
try:
    response = urllib2.urlopen(req)
    if doc['state'] != 'connected':
        doc['state'] = 'connected'
        res = db.save_doc(doc, force_update=True)
        add_history_item('Internet Connection restored', 'Internet should be working again', res['id'], res['rev'], 'connection_state', undoable=False)
except urllib2.URLError as e:
    if doc['state'] != 'disconnected':
        doc['state'] = 'disconnected'
        res = db.save_doc(doc, force_update=True)
        add_history_item('Internet connection error', str(e.reason), res['id'], res['rev'], 'connection_state', undoable=False)
