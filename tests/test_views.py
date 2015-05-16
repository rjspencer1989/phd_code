import unittest
from process_config import CouchdbConfigParser
from couchdbkit import *


class TestViews(unittest.TestCase):
    def test_notification_with_service(self):
        db = CouchdbConfigParser.getDB()
        doc1 = {
            "collection": "notifications",
            "name": "Rob",
            "service": "email",
            "user": "rob@robspencer.me.uk",
            "status": "done"
        }
        
        doc2 = {
            "collection": "notifications",
            "name": "Rob",
            "service": "growl",
            "user": "10.2.0.1",
            "status": "done"
        }
        
        res = db.save_doc(doc1)
        res2 = db.save_doc(doc2)
        vr = db.view("homework-remote/notification")
        vr_all = vr.all()
        print vr_all