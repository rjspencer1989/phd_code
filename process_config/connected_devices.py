#!/usr/bin/python
from couchdbkit import *
import couchdb_config_parser
import subprocess

db = couchdb_config_parser.get_db()
vr = db.view('homework-remote/valid_leases')
vra = vr.all()
for resItem in vra:
    cmd = ['ping', '-c2', resItem['value']]
    code = subprocess.call(cmd)
    doc = db.open_doc(resItem['id'])
    if code != 0:
        if doc['connection_event'] == 'connect':
            doc['connection_event'] = 'disconnect'
            doc['changed_by'] = 'connected_devices'
            db.save_doc(doc)
    else:
        if doc['connection_event'] == 'disconnect':
            doc['connection_event'] = 'connect'
            doc['changed_by'] = 'connected_devices'
            db.save_doc(doc)
