#!/usr/bin/python
from couchdbkit import *
import couchdb_config_parser
import subprocess

db = couchdb_config_parser.getDB()
vr = db.view('homework-remote/valid_leases')
vra = vr.all()
for resItem in vra:
    cmd = ['ping', '-c2', resItem['value']]
    code = subprocess.call(cmd)
    doc = db.open_doc(resItem['id'])
    if code == 0:
        doc['connected'] = True
    else:
        doc['connected'] = False
    doc['changed_by'] = 'system'
    db.save_doc(doc)
