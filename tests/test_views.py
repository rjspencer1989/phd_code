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
        key = ["Rob", "email"]
        vr = db.view("homework-remote/notification_with_service", key=key)
        vr_all = vr.all()
        l_vr_all = list(vr_all)
        self.assertEqual(len(l_vr_all), 1)
        res_obj = l_vr_all[0]
        self.assertEqual(res_obj['value'], doc1['user'])
        self.assertEqual(res_obj['id'], res['id'])
        db.delete_doc(res['id'])
        db.delete_doc(res2['id'])