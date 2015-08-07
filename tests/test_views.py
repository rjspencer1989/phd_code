import unittest
from process_config import couchdb_config_parser
from couchdbkit import *
import datetime
import time
from dateutil.tz import *


class TestViews(unittest.TestCase):
    def test_notification_with_service(self):
        db = couchdb_config_parser.get_db()
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
            "name": "Rob",
            "service": "email",
            "user": "psxrjs@exmail.nottingham.ac.uk",
            "status": "done",
            "hidden": True
        }

        res = db.save_doc(doc1)
        res2 = db.save_doc(doc2)
        res3 = db.save_doc(doc3)
        key = ["email", "Rob"]
        vr = db.view("homework-remote/notification_with_service", key=key)
        vr_all = vr.all()
        self.assertEqual(vr.count(), 1)
        res_obj = vr_all[0]
        self.assertEqual(res_obj['value'], doc1['user'])
        self.assertEqual(res_obj['id'], res['id'])
        doc1['hidden'] = True
        doc2['hidden'] = True
        db.save_doc(doc1, force_update=True)
        db.save_doc(doc2, force_update=True)

    def test_valid_leases(self):
        doc1 = {
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

        doc2 = {
            "action": "",
            "device_name": "psxrjs-mbp-eth",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.4",
            "mac_address": "68:a8:6d:3b:05:e5",
            "name": "Rob",
            "state": "permit",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "del",
            "device_type": "laptop",
            "notification_service": "email",
            "connection_event": "connect",
            "changed_by": "system"
        }

        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc1)
        res2 = db.save_doc(doc2)

        vr = db.view("homework-remote/valid_leases")
        vra = vr.all()
        self.assertEqual(vr.count(), 1)
        self.assertEqual(vra[0]['key'], '68:a8:6d:3b:05:e4')
        doc1['_deleted'] = True
        doc2['_deleted'] = True
        db.save_doc(doc1, force_update=True)
        db.save_doc(doc2, force_update=True)

    def test_events(self):
        doc = {
            "timestamp": datetime.datetime.now(tzutc()).isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "undoable": True,
            "perform_undo": False,
            "doc_collection": "devices",
            "action": "edit"
        }
        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc)
        vr = db.view("homework-remote/events")
        vra = vr.all()
        self.assertEqual(vr.count(), 1)
        self.assertEqual(vra[0]['id'], res['id'])
        doc['_deleted'] = True
        db.save_doc(doc, force_update=True)

    def test_dhcp(self):
        doc1 = {
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
        res = db.save_doc(doc1)
        vr = db.view("homework-remote/dhcp")
        vra = vr.all()
        self.assertEqual(vr.count(), 1)
        self.assertEqual(vra[0]['id'], res['id'])
        self.assertEqual(vra[0]['key'], "68:a8:6d:3b:05:e4")
        doc1['_deleted'] = True
        db.save_doc(doc1, force_update=True)

    def test_control(self):
        doc1 = {
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
        res = db.save_doc(doc1)
        vr = db.view("homework-remote/control")
        vra = vr.all()
        self.assertEqual(vr.count(), 1)
        self.assertEqual(vra[0]['id'], res['id'])
        self.assertEqual(vra[0]['key'], "connect")
        doc1['_deleted'] = True
        db.save_doc(doc1, force_update=True)

    def test_device_notification_service_mapping(self):
        doc1 = {
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
        res = db.save_doc(doc1)
        vr = db.view("homework-remote/device_notification_service_mapping")
        vra = vr.all()
        self.assertEqual(vr.count(), 1)
        self.assertEqual(vra[0]['id'], res['id'])
        self.assertEqual(vra[0]['key'], "68:a8:6d:3b:05:e4")
        self.assertEqual(vra[0]['value']['name'], "Rob")
        self.assertEqual(vra[0]['value']['service'], "email")
        doc1['_deleted'] = True
        db.save_doc(doc1, force_update=True)

    def test_connected_devices(self):
        doc1 = {
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

        doc2 = {
            "action": "",
            "device_name": "psxrjs-mbp-eth",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.4",
            "mac_address": "68:a8:6d:3b:05:e5",
            "name": "Rob",
            "state": "permit",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "del",
            "device_type": "laptop",
            "notification_service": "email",
            "connection_event": "disconnect",
            "changed_by": "system"
        }

        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc1)
        res2 = db.save_doc(doc2)
        vr = db.view("homework-remote/connected_devices")
        vra = vr.all()
        self.assertEqual(vr.count(), 1)
        self.assertEqual(vra[0]['id'], res['id'])
        self.assertEqual(vra[0]['key'], "68:a8:6d:3b:05:e4")
        doc1['_deleted'] = True
        db.save_doc(doc1, force_update=True)
        doc2['_deleted'] = True
        db.save_doc(doc2, force_update=True)

    def test_connected_devices_notification(self):
        doc1 = {
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

        doc2 = {
            "action": "",
            "device_name": "psxrjs-mbp-eth",
            "host_name": "psxrjs-mbp",
            "ip_address": "10.2.0.4",
            "mac_address": "68:a8:6d:3b:05:e5",
            "name": "Rob",
            "state": "permit",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "del",
            "device_type": "laptop",
            "notification_service": "email",
            "connection_event": "disconnect",
            "changed_by": "system"
        }

        doc3 = {
            "action": "",
            "device_name": "test_dev",
            "host_name": "test_dev",
            "ip_address": "10.2.0.1",
            "mac_address": "68:a8:6d:3b:05:e6",
            "name": "Rob",
            "state": "deny",
            "timestamp": time.time(),
            "collection": "devices",
            "lease_action": "add",
            "device_type": "laptop",
            "notification_service": "email",
            "connection_event": "connect",
            "changed_by": "system"
        }

        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc1)
        res2 = db.save_doc(doc2)
        res3 = db.save_doc(doc3)
        vr = db.view("homework-remote/connected_devices_for_notification")
        vra = vr.all()
        self.assertEqual(vr.count(), 1)
        self.assertEqual(vra[0]['id'], res['id'])
        self.assertEqual(vra[0]['key'], "68:a8:6d:3b:05:e4")
        doc1['_deleted'] = True
        db.save_doc(doc1, force_update=True)
        doc2['_deleted'] = True
        db.save_doc(doc2, force_update=True)
        doc3['_deleted'] = True
        db.save_doc(doc3, force_update=True)

    def test_undoable_events(self):
        doc1 = {
            "timestamp": datetime.datetime.now(tzutc()).isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "undoable": True,
            "perform_undo": False
        }

        doc2 = {
            "timestamp": datetime.datetime.now(tzutc()).isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "user": "Rob",
            "doc_id": "aabbccdd",
            "doc_rev": "1-aabbcc",
            "undoable": False,
            "perform_undo": False,
            "doc_collection": "notifications",
            "action": "add"
        }

        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc1)
        res2 = db.save_doc(doc2)
        vr = db.view("homework-remote/undoable_events")
        vra = vr.all()
        self.assertEqual(vr.count(), 1)
        self.assertEqual(vra[0]['id'], res['id'])
        doc1['_deleted'] = True
        db.save_doc(doc1, force_update=True)
        doc2['_deleted'] = True
        db.save_doc(doc2, force_update=True)
