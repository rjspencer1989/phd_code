import unittest
from process_config import CouchdbConfigParser
import datetime
import time


class TestValidation(unittest.TestCase):
    def test_no_collection(self):
        doc = {"foo": "bar"}
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_collection(self):
        doc = {
            "name":"Rob",
            "service":"email",
            "userdetails":"rob@robspencer.me.uk",
            "collection": "notify"
        }
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_notification_valid(self):
        doc = {
            "name" : "Rob",
            "service" : "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "pending"
        }
        db = CouchdbConfigParser.getDB()
        db.save_doc(doc)

    def test_notification_invalid_status(self):
        doc = {
            "name" : "Rob",
            "service" : "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "foo"
        }
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_required(self):
        doc = {
            "service" : "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "foo"
        }
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_unchanged(self):
        doc = {
            "name" : "Rob",
            "service" : "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "pending"
        }
        db = CouchdbConfigParser.getDB()
        db.save_doc(doc)
        doc['name'] = 'test'
        with self.assertRaises(Exception):
            db.save_doc(doc, force_update=True)

    def test_event(self):
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
        db.save_doc(doc)

    def test_event_not_undoable(self):
        doc = {
            "timestamp" : datetime.datetime.now().isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "undoable": False,
            "perform_undo": False
        }
        db = CouchdbConfigParser.getDB()
        db.save_doc(doc)

    def test_valid_device(self):
        doc = {
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
        db = CouchdbConfigParser.getDB()
        db.save_doc(doc)

    def test_invalid_lease_action(self):
        doc = {
            "action":"",
            "device_name": "psxrjs-mbp",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.1",
            "mac_address" : "68:a8:6d:3b:05:e4",
            "name": "Rob",
            "state": "permit",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "rm",
            "device_type": "laptop",
            "notification_service": "email"
        }
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_action(self):
        doc = {
            "action":"blacklist",
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
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_state(self):
        doc = {
            "action":"",
            "device_name": "psxrjs-mbp",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.1",
            "mac_address" : "68:a8:6d:3b:05:e4",
            "name": "Rob",
            "state": "blacklist",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "add",
            "device_type": "laptop",
            "notification_service": "email"
        }
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_valid_wifi(self):
        doc = {
            "collection" : "wifi",
            "status": "pending",
            "ssid": "spencer"
        }
        db = CouchdbConfigParser.getDB()
        db.save_doc(doc)