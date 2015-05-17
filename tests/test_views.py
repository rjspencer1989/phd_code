import unittest
from process_config import CouchdbConfigParser
from couchdbkit import *

import time

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

    def test_notification_names(self):
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
        
        doc3 = {
            "collection": "notifications",
            "name": "Harry",
            "service": "email",
            "user": "harrye@robspencer.me.uk",
            "status": "done"
        }

        res = db.save_doc(doc1)
        res2 = db.save_doc(doc2)
        res3 = db.save_doc(doc3)
        vr = db.view("homework-remote/notification_names", group=True)
        vra = vr.all()
        l_vra = list(vra)
        self.assertEqual(len(l_vra), 2)
        self.assertEqual(l_vra[0]['key'], 'Harry')
        self.assertEqual(l_vra[1]['key'], 'Rob')
        db.delete_doc(res['id'])
        db.delete_doc(res2['id'])
        db.delete_doc(res3['id'])

    def test_valid_leases(self):
        doc1 = {
           "action":"",
           "device_name": "psxrjs-mbp",
           "host_name": "psxrjs-mbp",
           "ip_address": "10.2.0.1",
           "mac_address" : "68:a8:6d:3b:05:e4",
           "name": "Rob",
           "state": "permit",
           "timestamp": time.time(),
           "collection": "devices",
           "lease_action": "add",
           "device_type": "laptop",
           "notification_service": "email"
        }
        
        doc2 = {
           "action":"",
           "device_name": "psxrjs-mbp-eth",
           "host_name": "psxrjs-mbp",
           "ip_address": "10.2.0.4",
           "mac_address" : "68:a8:6d:3b:05:e5",
           "name": "Rob",
           "state": "permit",
           "timestamp": time.time(),
           "collection": "devices",
           "lease_action": "del",
           "device_type": "laptop",
           "notification_service": "email"
        }

        db = CouchdbConfigParser.getDB()
        res = db.save_doc(doc1)
        res2 = db.save_doc(doc2)

        vr = db.view("homework-remote/valid_leases")
        vra = vr.all()
        vra_l = list(vra)
        self.assertEqual(len(vra_l), 1)
        self.assertEqual(vra_l[0]['key'], '68:a8:6d:3b:05:e4')
        db.delete_doc(res['id'])
        db.delete_doc(res2['id'])

    def test_events(self):
        doc = {
            "timestamp" : datetime.datetime.now().isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "undoable": True,
            "perform_undo": False
        }
        db = CouchdbConfigParser.getDB()
        res = db.save_doc(doc)
        vr = db.view("homework-remote/events")
        vra = vr.all()
        l_vra = list(vra)
        self.assertEqual(len(l_vra), 1)
        self.assertEqual(l_vra[0]['id'], res['id'])
        db.delete_doc(res['id'])