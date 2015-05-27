import unittest
import time
import datetime
from process_config import couchdb_config_parser
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
            "connected": False,
            "changed_by": "user"
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
            "connected": False,
            "changed_by": "system"
        }
        db = couchdb_config_parser.get_db()
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
            "connected": False,
            "changed_by": "user"
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
            "connected": False,
            "changed_by": "system"
        }
        db = couchdb_config_parser.get_db()
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
            "service": "email",
            "body": "test"
        }

        not_inc = {
            "collection": "notification-request",
            "status": "done",
            "to": "Rob",
            "service": "email",
            "body": "test"
        }

        db = couchdb_config_parser.get_db()
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

        db = couchdb_config_parser.get_db()
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
            "timestamp": datetime.datetime.now().isoformat()
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
            "timestamp": datetime.datetime.now().isoformat()
        }

        not_inc = {
            "collection": "events",
            "perform_undo": False,
            "undoable": False,
            "title": "test",
            "description": "test",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "4-aabbcc",
            "timestamp": datetime.datetime.now().isoformat()
        }

        db = couchdb_config_parser.get_db()
        res = db.save_doc(inc)
        res2 = db.save_doc(not_inc_not_perform_undo)
        res3 = db.save_doc(not_inc)
        stream = ChangesStream(db, filter="homework-remote/undo")
        self.assertTrue((len(list(stream)) == 1) and (res['id'] == list(stream)[0]['id']))
        db.delete_doc(res['id'])
        db.delete_doc(res2['id'])
        db.delete_doc(res3['id'])

    def test_wifi(self):
        inc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "encryption_type": "wep",
            "channel": 1,
            "mode": "g",
            "password_type": "txt",
            "password": "whatever12345"
        }

        not_inc = {
            "collection": "wifi",
            "status": "done",
            "ssid": "spencer",
            "encryption_type": "wep",
            "channel": 1,
            "mode": "g",
            "password_type": "txt",
            "password": "whatever12345"
        }

        db = couchdb_config_parser.get_db()
        res = db.save_doc(inc)
        res2 = db.save_doc(not_inc)
        stream = ChangesStream(db, filter="homework-remote/wifi")
        self.assertTrue((len(list(stream)) == 1) and (res['id'] == list(stream)[0]['id']))
        db.delete_doc(res['id'])
        db.delete_doc(res2['id'])

    def test_revert(self):
        inc = {
            "collection": "request_revert",
            "status": "pending",
            "timestamp": "2015-05-27T14:10:53.829Z"
        }

        not_inc = {
            "collection": "request_revert",
            "status": "done",
            "timestamp": "2015-05-27T14:10:53.829Z"
        }

        db = couchdb_config_parser.get_db()
        res = db.save_doc(inc)
        res2 = db.save_doc(not_inc)
        stream = ChangesStream(db, filter="homework-remote/revert")
        self.assertTrue((len(list(stream)) == 1) and (res['id'] == list(stream)[0]['id']))
        db.delete_doc(res['id'])
        db.delete_doc(res2['id'])
