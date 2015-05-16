import unittest
import time
from process_config import CouchdbConfigParser
from couchdbkit.changes import ChangesStream


class TestFilters(unittest.TestCase):
    def test_devices_pox(self):
        inc = {
            "_id": "aa:bb:cc:dd:ee:ff",
            "action": "permit",
            "collection": "devices",
            "device_name": "test-device",
            "host_name": "test-device",
            "ip_address": "10.2.0.61",
            "lease_action": "add",
            "mac_address": "aa:bb:cc:dd:ee:ff",
            "name": "Rob",
            "state": "pending",
            "device_type": "laptop",
            "notification_service": "email",
            "timestamp": time.time(),
            "connected": False
        }

        not_inc = {
            "_id": "ab:bc:cd:de:ef:fa",
            "action": "",
            "collection": "devices",
            "device_name": "test-device2",
            "host_name": "test-device",
            "ip_address": "10.2.0.65",
            "lease_action": "add",
            "mac_address": "ab:bc:cd:de:ef:fa",
            "name": "Rob",
            "state": "permit",
            "device_type": "laptop",
            "notification_service": "twitter",
            "timestamp": time.time(),
            "connected": False
        }
        db = CouchdbConfigParser.getDB()
        db.save_doc(inc)
        db.save_doc(not_inc)
        stream = ChangesStream(db, filter="homework-remote/devices_pox")
        self.assertTrue((len(list(stream)) == 1) and ('aa:bb:cc:dd:ee:ff' == list(stream)[0]['id']))
        db.delete_doc("aa:bb:cc:dd:ee:ff")
        db.delete_doc("ab:bc:cd:de:ef:fa")

    def test_devices_ui(self):
        not_inc = {
            "_id": "aa:bb:cc:dd:ee:ff",
            "action": "permit",
            "collection": "devices",
            "device_name": "test-device",
            "host_name": "test-device",
            "ip_address": "10.2.0.61",
            "lease_action": "add",
            "mac_address": "aa:bb:cc:dd:ee:ff",
            "name": "Rob",
            "state": "pending",
            "device_type": "laptop",
            "notification_service": "email",
            "timestamp": time.time(),
            "connected": False
        }

        inc = {
            "_id": "ab:bc:cd:de:ef:fa",
            "action": "",
            "collection": "devices",
            "device_name": "test-device2",
            "host_name": "test-device",
            "ip_address": "10.2.0.65",
            "lease_action": "add",
            "mac_address": "ab:bc:cd:de:ef:fa",
            "name": "Rob",
            "state": "permit",
            "device_type": "laptop",
            "notification_service": "twitter",
            "timestamp": time.time(),
            "connected": False
        }
        db = CouchdbConfigParser.getDB()
        db.save_doc(inc)
        db.save_doc(not_inc)
        stream = ChangesStream(db, filter="homework-remote/devices_ui")
        self.assertTrue((len(list(stream)) == 1) and ('ab:bc:cd:de:ef:fa' == list(stream)[0]['id']))
        db.delete_doc("aa:bb:cc:dd:ee:ff")
        db.delete_doc("ab:bc:cd:de:ef:fa")

    def test_notification_request(self):
        inc = {
            "collection": "notification-request",
            "status": "pending",
            "to": "Rob",
            "service":"email",
            "body": "test"
        }

        not_inc = {
            "collection": "notification-request",
            "status": "done",
            "to": "Rob",
            "service":"email",
            "body": "test"
        }

        db = CouchdbConfigParser.getDB()
        res = db.save_doc(inc)
        res2 = db.save_doc(not_inc)
        stream = ChangesStream(db, filter="homework-remote/notification_request")
        self.assertTrue((len(list(stream)) == 1) and (res['id'] == list(stream)[0]['id']))
        db.delete_doc(res['id'])
        db.delete_doc(res2['id'])

    def test_notifications(self):
        inc = {
            "collection": "notifications",
            "status": "pending",
            "name": "Rob",
            "service": "email",
            "user": "signup@robspencer.me.uk"
        }

        not_inc = {
            "collection": "notifications",
            "status": "done",
            "name": "Rob",
            "service": "email",
            "user": "signup@robspencer.me.uk"
        }

        db = CouchdbConfigParser.getDB()
        res = db.save_doc(inc)
        res2 = db.save_doc(not_inc)
        stream = ChangesStream(db, filter="homework-remote/notifications")
        self.assertTrue((len(list(stream)) == 1) and (res['id'] == list(stream)[0]['id']))
        db.delete_doc(res['id'])
        db.delete_doc(res2['id'])

    def test_undo(self):
        inc = {
            "collection": "events",
            "perform_undo": True,
            "undoable": True,
            "title": "test",
            "description": "test",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "timestamp": time.time()
        }

        not_inc_not_perform_undo = {
            "collection": "events",
            "perform_undo": False,
            "undoable": True,
            "title": "test",
            "description": "test",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "2-aabbcc",
            "timestamp": time.time()
        }

        not_inc_not_undoable = {
            "collection": "events",
            "perform_undo": True,
            "undoable": False,
            "title": "test",
            "description": "test",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "3-aabbcc",
            "timestamp": time.time()
        }

        not_inc = {
            "collection": "events",
            "perform_undo": True,
            "undoable": True,
            "title": "test",
            "description": "test",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "timestamp": time.time()
        }

        db = CouchdbConfigParser.getDB()
        res = db.save_doc(inc)
        res2 = db.save_doc(not_inc_not_perform_undo)
        res3 = db.save_doc(not_inc_not_undoable)
        res4 = db.save_doc(not_inc)
        stream = ChangesStream(db, filter="homework-remote/undo")
        for change in stream:
            print change
        self.assertTrue((len(list(stream)) == 1) and (res['id'] == list(stream)[0]['id']))
        db.delete_doc(res['id'])
        db.delete_doc(res2['id'])
        db.delete_doc(res3['id'])
        db.delete_doc(res4['id'])
