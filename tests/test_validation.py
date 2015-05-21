import unittest
from process_config import couchdb_config_parser
import datetime
import time


class TestValidation(unittest.TestCase):
    def test_no_collection(self):
        doc = {"foo": "bar"}
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_collection(self):
        doc = {
            "name": "Rob",
            "service": "email",
            "userdetails": "rob@robspencer.me.uk",
            "collection": "notify"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_notification_valid(self):
        doc = {
            "name": "Rob",
            "service": "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "pending"
        }
        db = couchdb_config_parser.getDB()
        res = db.save_doc(doc)
        db.delete_doc(res['id'])

    def test_notification_invalid_status(self):
        doc = {
            "name": "Rob",
            "service": "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "foo"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_required(self):
        doc = {
            "service": "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "foo"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_unchanged(self):
        doc = {
            "name": "Rob",
            "service": "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "pending"
        }
        db = couchdb_config_parser.getDB()
        db.save_doc(doc)
        doc['name'] = 'test'
        with self.assertRaises(Exception):
            db.save_doc(doc, force_update=True)

    def test_event(self):
        doc = {
            "timestamp": datetime.datetime.now().isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "undoable": True,
            "perform_undo": False
        }
        db = couchdb_config_parser.getDB()
        res = db.save_doc(doc)
        db.delete_doc(res['id'])

    def test_event_not_undoable(self):
        doc = {
            "timestamp": datetime.datetime.now().isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "undoable": False,
            "perform_undo": False
        }
        db = couchdb_config_parser.getDB()
        res = db.save_doc(doc)
        db.delete_doc(res['id'])

    def test_event_perform_undo_not_undoable(self):
        doc = {
            "timestamp": datetime.datetime.now().isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "undoable": False,
            "perform_undo": True
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_valid_device(self):
        doc = {
            "action": "",
            "device_name": "psxrjs-mbp",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.1",
            "mac_address": "68:a8:6d:3b:05:e4",
            "name": "Rob",
            "state": "permit",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "add",
            "device_type": "laptop",
            "notification_service": "email",
            "connected": True,
            "changed_by": "system"
        }
        db = couchdb_config_parser.getDB()
        res = db.save_doc(doc)
        db.delete_doc(res['id'])

    def test_invalid_lease_action(self):
        doc = {
            "action": "",
            "device_name": "psxrjs-mbp",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.1",
            "mac_address": "68:a8:6d:3b:05:e4",
            "name": "Rob",
            "state": "permit",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "rm",
            "device_type": "laptop",
            "notification_service": "email",
            "connected": True,
            "changed_by": "system"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_action(self):
        doc = {
            "action": "blacklist",
            "device_name": "psxrjs-mbp",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.1",
            "mac_address": "68:a8:6d:3b:05:e4",
            "name": "Rob",
            "state": "permit",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "add",
            "device_type": "laptop",
            "notification_service": "email",
            "connected": True,
            "changed_by": "system"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_state(self):
        doc = {
            "action": "",
            "device_name": "psxrjs-mbp",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.1",
            "mac_address": "68:a8:6d:3b:05:e4",
            "name": "Rob",
            "state": "blacklist",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "add",
            "device_type": "laptop",
            "notification_service": "email",
            "connected": True,
            "changed_by": "system"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_valid_wifi(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "txt",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.getDB()
        res = db.save_doc(doc)
        db.delete_doc(res['id'])

    def test_invalid_mode(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "a",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "txt",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_encryption_type(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wpa",
            "password_type": "txt",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_status(self):
        doc = {
            "collection": "wifi",
            "status": "finished",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "txt",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_empty_ssid(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "txt",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_long_ssid(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "abcdefghijklmnopqrstuvwxyz1234567890",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "txt",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_low_channel(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": -1,
            "encryption_type": "wep",
            "password_type": "txt",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_high_channel(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 12,
            "encryption_type": "wep",
            "password_type": "txt",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_password_type(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "text",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_txt_password_5_chars(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "txt",
            "password": "whate"
        }
        db = couchdb_config_parser.getDB()
        res = db.save_doc(doc)
        db.delete_doc(res['id'])

    def test_txt_password_13_chars(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "txt",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.getDB()
        res = db.save_doc(doc)
        db.delete_doc(res['id'])

    def test_txt_password_invalid(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "txt",
            "password": "whatever"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_hex_password_10_chars(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "hex",
            "password": "1234567890"
        }
        db = couchdb_config_parser.getDB()
        res = db.save_doc(doc)
        db.delete_doc(res['id'])

    def test_hex_password_26_chars(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "hex",
            "password": "1234567890abcdef0123456789"
        }
        db = couchdb_config_parser.getDB()
        res = db.save_doc(doc)
        db.delete_doc(res['id'])

    def test_hex_password_invalid_length(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "hex",
            "password": "123456789"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_hex_password_invalid_hex(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "hex",
            "password": "123456789t"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_hex_password_invalid_hex_and_length(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password_type": "hex",
            "password": "12345678q"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_valid_notification_request(self):
        doc = {
            "collection": "notification-request",
            "to": "Rob",
            "service": "email",
            "body": "message",
            "status": "pending"
        }
        db = couchdb_config_parser.getDB()
        res = db.save_doc(doc)
        db.delete_doc(res['id'])

    def test_empty_string(self):
        doc = {
            "collection": "notification-request",
            "to": "",
            "service": "email",
            "body": "message",
            "status": "pending"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_notification_request_status_invalid(self):
        doc = {
            "collection": "notification-request",
            "to": "Rob",
            "service": "email",
            "body": "message",
            "status": "complete"
        }
        db = couchdb_config_parser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)
