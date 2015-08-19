import unittest
from process_config import couchdb_config_parser, perform_rollback, add_history, notification_registration_client, edit_wifi
import datetime
import mock
from dateutil.tz import tzutc
import pprint


class TestProcessRollback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = couchdb_config_parser.get_db()

    @classmethod
    def tearDownClass(cls):
        cls.db = None

    def setUp(self):
        self.test_doc_ids = []
        self.title = "test rollback"
        self.description = "test rollback description"
        self.wifi_doc = {
            "collection": "wifi",
            "status": "done",
            "ssid": "testing",
            "mode": "g",
            "encryption_type": "wpa",
            "password_type": "txt",
            "password": "whatever12345",
            "channel": 1,
            "with_bss": False
        }
        self.notification_doc = {
            "collection": "notifications",
            "name": "Rob",
            "service": "phone",
            "user": "+447972058628",
            "status": "done"
        }
        self.revert_doc = {
            "collection": "request_revert",
            "timestamp": datetime.datetime(2015, 1, 20).isoformat(),
            "status": "pending"
        }
        dt = datetime.datetime(2015, 1, 5, hour=10, minute=5)
        self.wifi_doc['event_timestamp'] = dt.isoformat()
        res1 = self.db.save_doc(self.wifi_doc)
        self.wifi_doc = self.db.get(res1['id'])
        edit_wifi.process_wifi(self.wifi_doc)
        self.test_doc_ids.append(res1['id'])
        self.wifi_doc = self.db.get(res1['id'])
        self.wifi_doc['ssid'] = 'testing2'
        res2 = self.db.save_doc(self.wifi_doc)
        dt = datetime.datetime(2015, 2, 5, hour=10, minute=5)
        self.wifi_doc['ssid'] = 'testing3'
        res3 = self.db.save_doc(self.wifi_doc)
        dt = datetime.datetime(2015, 2, 23, hour=15, minute=0)
        self.notification_doc['event_timestamp'] = dt.isoformat()
        res4 = self.db.save_doc(self.notification_doc)
        self.test_doc_ids.append(res4['id'])
        self.notification_doc = self.db.get(res4['id'])
        notification_registration_client.registration(self.notification_doc)
        dt = datetime.datetime(2015, 2, 12, hour=14, minute=34)
        self.notification_doc = self.db.get(res4['id'])
        self.rb = perform_rollback.Rollback(self.db, self.revert_doc)

    def tearDown(self):
        for doc in self.test_doc_ids:
            opened = self.db.get(doc)
            opened['_deleted'] = True
            self.db.save_doc(opened, force_update=True)
        current_events = self.db.view('homework-remote/events')
        if current_events.count() > 0:
            current_events_all = current_events.all()
            for row in current_events_all:
                current_doc = self.db.get(row['id'])
                current_doc['_deleted'] = True
                self.db.save_doc(current_doc, force_update=True)

    def test_process_rollback_get_events(self):
        print self.revert_doc['timestamp']
        result = self.rb.get_events_after_timestamp(self.revert_doc['timestamp'])
        pprint.pprint(result)
        result_list = list(result)
        self.assertEqual(3, len(result_list))

    def test_process_rollback_get_docs_to_revert(self):
        result = self.rb.get_docs_to_revert(self.revert_doc['timestamp'])
        pprint.pprint(result)
        self.assertEqual(2, len(result))
        k = result.keys()
        self.assertNotEqual(k[0], k[1])

    def test_rollback(self):
        result = self.rb.revert(self.revert_doc['timestamp'])
        self.assertTrue(result)
