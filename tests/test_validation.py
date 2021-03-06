# coding=utf-8
import unittest
from process_config import couchdb_config_parser
import datetime
import time
from dateutil.tz import *


class TestValidation(unittest.TestCase):
    def test_no_collection(self):
        doc = {"foo": "bar"}
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_collection(self):
        doc = {
            "name": "Rob",
            "service": "email",
            "userdetails": "rob@robspencer.me.uk",
            "collection": "notify"
        }
        db = couchdb_config_parser.get_db()
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
        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc)
        doc['_deleted'] = True
        db.save_doc(doc, force_update=True)

    def test_notification_invalid_email(self):
        doc = {
            "name": "Rob",
            "service": "email",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "pending"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_notification_invalid_status(self):
        doc = {
            "name": "Rob",
            "service": "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "foo"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_required(self):
        doc = {
            "service": "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "foo"
        }
        db = couchdb_config_parser.get_db()
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
        db = couchdb_config_parser.get_db()
        db.save_doc(doc)
        doc['name'] = 'test'
        with self.assertRaises(Exception):
            db.save_doc(doc, force_update=True)

    def test_event(self):
        doc = {
            "timestamp": datetime.datetime.now(tzutc()).isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "docs": [{
                "doc_id": "aabbcc",
                "doc_rev": "1-aabbcc",
                "doc_collection": "devices",
                "action": "edit"
            }],
            "undoable": True,
            "perform_undo": False
        }
        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc)
        doc['_deleted'] = True
        db.save_doc(doc, force_update=True)

    def test_event_not_undoable(self):
        doc = {
            "timestamp": datetime.datetime.now(tzutc()).isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "docs": [{
                "doc_id": "aabbcc",
                "doc_rev": "1-aabbcc",
                "doc_collection": "devices",
                "action": "edit"
            }],
            "undoable": False,
            "perform_undo": False
        }
        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc)
        doc['_deleted'] = True
        db.save_doc(doc, force_update=True)

    def test_event_perform_undo_not_undoable(self):
        doc = {
            "timestamp": datetime.datetime.now(tzutc()).isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "undoable": False,
            "perform_undo": True,
            "doc_collection": "devices",
            "action": "edit"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_event_no_doc_collection(self):
        doc = {
            "timestamp": datetime.datetime.now(tzutc()).isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "undoable": False,
            "perform_undo": True,
            "action": "edit"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_event_no_action(self):
        doc = {
            "timestamp": datetime.datetime.now(tzutc()).isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "undoable": False,
            "perform_undo": True,
            "doc_collection": "devices"
        }
        db = couchdb_config_parser.get_db()
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
            "connection_event": "connect",
            "changed_by": "system"
        }
        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc)
        doc['_deleted'] = True
        db.save_doc(doc, force_update=True)

    def test_invalid_mac_address(self):
        doc = {
            "action": "",
            "device_name": "",
            "host_name": "",
            "ip_address": "",
            "mac_address": "",
            "name": "Rob",
            "state": "permit",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "add",
            "device_type": "",
            "notification_service": "",
            "connection_event": "disconnect",
            "changed_by": "system"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

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
            "connection_event": "connect",
            "changed_by": "system"
        }
        db = couchdb_config_parser.get_db()
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
            "connection_event": "connect",
            "changed_by": "system"
        }
        db = couchdb_config_parser.get_db()
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
            "connection_event": "connect",
            "changed_by": "system"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_valid_wifi(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wpa",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc)
        doc['_deleted'] = True
        db.save_doc(doc, force_update=True)

    def test_invalid_mode(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "a",
            "channel": 1,
            "encryption_type": "wpa",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_encryption_type(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wep",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_status(self):
        doc = {
            "collection": "wifi",
            "status": "finished",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wpa",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_empty_ssid(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wpa",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_long_ssid(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "abcdefghijklmnopqrstuvwxyz1234567890",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wpa",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_low_channel(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": -1,
            "encryption_type": "wpa",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_high_channel(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 12,
            "encryption_type": "wpa",
            "password": "whatever12345"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_password_7_chars(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wpa",
            "password": "whateve"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_txt_password_8_chars(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wpa",
            "password": "whatever"
        }
        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc)
        doc['_deleted'] = True
        db.save_doc(doc, force_update=True)

    def test_password_64_chars(self):
        pw = "whateverwhateverwhateverwhateverwhateverwhateverwhateverwhatever"
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wpa",
            "password": pw
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_password_non_ascii_chars(self):
        doc = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "spencer",
            "mode": "g",
            "channel": 1,
            "encryption_type": "wpa",
            "password": "whatever±"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_valid_notification_request(self):
        doc = {
            "collection": "request_notification",
            "to": "Rob",
            "service": "email",
            "body": "message",
            "status": "pending"
        }
        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc)
        doc['_deleted'] = True
        db.save_doc(doc, force_update=True)

    def test_empty_string(self):
        doc = {
            "collection": "notification-request",
            "to": "",
            "service": "email",
            "body": "message",
            "status": "pending"
        }
        db = couchdb_config_parser.get_db()
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
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_valid_rollback_request(self):
        doc = {
            "collection": "request_revert",
            "timestamp": datetime.datetime.now(tzutc()).isoformat(),
            "status": "pending"
        }

        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc)
        doc['_deleted'] = True
        db.save_doc(doc, force_update=True)

    def test_rollback_invalid_status(self):
        doc = {
            "collection": "request_revert",
            "timestamp": datetime.datetime.now(tzutc()).isoformat(),
            "status": "waiting"
        }

        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_rollback_invalid_timestamp(self):
        doc = {
            "collection": "request_revert",
            "timestamp": '2015-14-27T15:19:06.690Z',
            "status": "pending"
        }

        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_device_set_name_when_pending(self):
        doc = {
            "action": "",
            "device_name": "",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.1",
            "mac_address": "68:a8:6d:3b:05:e4",
            "name": "Rob",
            "state": "pending",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "add",
            "device_type": "",
            "notification_service": "",
            "connection_event": "connect",
            "changed_by": "user"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_device_set_device_name_when_pending(self):
        doc = {
            "action": "",
            "device_name": "psxrjs-mbp",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.1",
            "mac_address": "68:a8:6d:3b:05:e4",
            "name": "",
            "state": "pending",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "add",
            "device_type": "",
            "notification_service": "",
            "connection_event": "connect",
            "changed_by": "user"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_device_set_device_type_when_pending(self):
        doc = {
            "action": "",
            "device_name": "",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.1",
            "mac_address": "68:a8:6d:3b:05:e4",
            "name": "",
            "state": "pending",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "add",
            "device_type": "laptop",
            "notification_service": "",
            "connection_event": "connect",
            "changed_by": "user"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_device_set_notification_service_when_pending(self):
        doc = {
            "action": "",
            "device_name": "",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.1",
            "mac_address": "68:a8:6d:3b:05:e4",
            "name": "",
            "state": "pending",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "add",
            "device_type": "",
            "notification_service": "email",
            "connection_event": "connect",
            "changed_by": "user"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_device_set_name_and_device_name_when_pending(self):
        doc = {
            "action": "",
            "device_name": "psxrjs-mbp",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.1",
            "mac_address": "68:a8:6d:3b:05:e4",
            "name": "Rob",
            "state": "pending",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "add",
            "device_type": "",
            "notification_service": "",
            "connection_event": "connect",
            "changed_by": "user"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_device_set_metadata_when_pending(self):
        doc = {
            "action": "",
            "device_name": "psxrjs-mbp",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.1",
            "mac_address": "68:a8:6d:3b:05:e4",
            "name": "Rob",
            "state": "pending",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "add",
            "device_type": "laptop",
            "notification_service": "email",
            "connection_event": "connect",
            "changed_by": "user"
        }
        db = couchdb_config_parser.get_db()
        with self.assertRaises(Exception):
            db.save_doc(doc)
