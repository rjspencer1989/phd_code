import unittest
from process_config import couchdb_config_parser, perform_rollback, notification_registration_client
from process_config.add_history import add_history_item
from undo import perform_undo
from undo.doc_types import request_revert
import time
import pprint
import datetime


class TestUndoRollback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = couchdb_config_parser.get_db()

        cls.test_doc_ids = []
        cls.title = "test rollback"
        cls.description = "test rollback description"
        cls.wifi_doc = {
            "collection": "wifi",
            "status": "done",
            "ssid": "testing",
            "mode": "g",
            "encryption_type": "wpa",
            "password_type": "txt",
            "password": "whatever12345",
            "channel": 1
        }
        cls.notification_doc = {
            "collection": "notifications",
            "name": "Rob",
            "service": "phone",
            "user": "+447972058628",
            "status": "done"
        }
        cls.revert_doc = {
            "collection": "request_revert",
            "timestamp": datetime.datetime(2015, 1, 20).isoformat(),
            "status": "pending"
        }
        dt = datetime.datetime(2015, 1, 5, hour=10, minute=5)
        cls.wifi_doc['event_timestamp'] = dt.isoformat()
        res1 = cls.db.save_doc(cls.wifi_doc)
        cls.test_doc_ids.append(res1['id'])
        cls.wifi_doc['ssid'] = 'testing2'
        dt = datetime.datetime(2015, 2, 5, hour=10, minute=5)
        cls.wifi_doc['event_timestamp'] = dt.isoformat()
        res2 = cls.db.save_doc(cls.wifi_doc)
        cls.wifi_doc['ssid'] = 'testing3'
        res3 = cls.db.save_doc(cls.wifi_doc)
        dt = datetime.datetime(2015, 2, 23, hour=15, minute=0)
        cls.notification_doc['event_timestamp'] = dt.isoformat()
        res4 = cls.db.save_doc(cls.notification_doc)
        cls.notification_doc = cls.db.get(res4['id'])
        notification_registration_client.registration(cls.notification_doc)
        cls.test_doc_ids.append(res4['id'])
        cls.revert_res = cls.db.save_doc(cls.revert_doc)
        cls.revert_doc = cls.db.get(cls.revert_res['id'])
        cls.test_doc_ids.append(cls.revert_res['id'])
        cls.notification_doc = cls.db.get(cls.notification_doc['_id'])
        dt = datetime.datetime(2015, 2, 12, hour=14, minute=34)
        cls.rb = perform_rollback.Rollback(cls.db, cls.revert_doc)
        cls.rb.revert(cls.revert_doc['timestamp'])
        rd = cls.db.get(cls.revert_doc['_id'], revs_info=True)
        dt = datetime.datetime(2015, 7, 23, hour=15, minute=0)
        cls.rd_hist = add_history_item("unrev", "unrev", rd['_id'], rd['_rev'], 'request_revert', ts=dt.isoformat())
        cls.test_doc_ids.append(cls.rd_hist['id'])
        cls.undo_revert = request_revert.Request_revert(rd, cls.db.get(cls.rd_hist['id']))

    @classmethod
    def tearDownClass(cls):
        for doc in cls.test_doc_ids:
            opened = cls.db.get(doc)
            opened['_deleted'] = True
            cls.db.save_doc(opened, force_update=True)
        current_events = cls.db.view('homework-remote/events')
        if current_events.count() > 0:
            current_events_all = current_events.all()
            for row in current_events_all:
                current_doc = cls.db.get(row['id'])
                current_doc['_deleted'] = True
                cls.db.save_doc(current_doc, force_update=True)
        cls.db = None

    def test_get_events(self):
        result = self.undo_revert.get_events(self.revert_doc['timestamp'])
        vra = result.all()
        pprint.pprint(vra)
        self.assertEqual(4, result.count())

    def test_get_reverted_events(self):
        result = self.undo_revert.get_reverted_events()
        pprint.pprint(result)
