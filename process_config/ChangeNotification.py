#!/usr/bin/env python
from couchdbkit import *
import CouchdbConfigParser

def sendNotification(to, service, message):
    db = CouchdbConfigParser.getDB()
    doc = {}
    doc['to'] = to
    doc['service'] = service
    doc['status'] = 'pending'
    doc['body'] = message
    db.save_doc(doc)
