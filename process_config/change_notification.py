#!/usr/bin/env python
from couchdbkit import *
import couchdb_config_parser


def sendNotification(to, service, message):
    db = couchdb_config_parser.getDB()
    doc = {}
    doc['to'] = to
    doc['service'] = service
    doc['status'] = 'pending'
    doc['body'] = message
    doc['collection'] = 'notification-request'
    res = db.save_doc(doc)
    return res
