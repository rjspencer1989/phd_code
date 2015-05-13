#!/usr/bin/python
from couchdbkit import *
import CouchdbConfigParser
import subprocess

db = CouchdbConfigParser.getDB()
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
    db.save_doc(doc)
