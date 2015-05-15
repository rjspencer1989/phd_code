import unittest
import time
from process_config import CouchdbConfigParser
from couchdbkit.changes import ChangesStream


class TestFilters(unittest.TestCase):
    def test_devices_pox(self):
        inc = {
            action: "permit",
            collection: "devices",
            device_name: "test-device",
            host_name: "test-device",
            ip_address: "10.2.0.61",
            lease_action: "add",
            mac_address: "aa:bb:cc:dd:ee:ff",
            name: "",
            state: "pending",
            device_type: "",
            notification_service: "",
            timestamp: time.time(),
            connected: False
        }

        not_inc = {
            action: "",
            collection: "devices",
            device_name: "test-device",
            host_name: "test-device",
            ip_address: "10.2.0.61",
            lease_action: "add",
            mac_address: "aa:bb:cc:dd:ee:ff",
            name: "",
            state: "permit",
            device_type: "",
            notification_service: "",
            timestamp: time.time(),
            connected: False
        }
        db = CouchdbConfigParser.getDB()
        d1 = db.save_doc(inc)
        d2 = db.save_doc(not_inc)
        stream = ChangesStream(db)
        for change in stream:
            print change
        db.delete_doc(d1['id'])
        db.delete_doc(d1['id'])
