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
            "_id": "ab:bc:cd:de:ef:fa"
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
        d1 = db.save_doc(inc)
        d2 = db.save_doc(not_inc)
        stream = ChangesStream(db)
        for change in stream:
            print change
        db.delete_doc(d1['id'])
        db.delete_doc(d1['id'])
