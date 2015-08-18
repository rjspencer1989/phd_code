import unittest
from process_config import couchdb_config_parser, perform_rollback, add_history, notification_registration_client
import datetime
import mock
from dateutil.tz import tzutc


class TestProcessRollback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = couchdb_config_parser.get_db()
        current_events = cls.db.view('homework-remote/events')
        if current_events.count() > 0:
            current_events_all = current_events.all()
            for row in current_events_all:
                current_doc = cls.db.get(row['id'])
                current_doc['_deleted'] = True
                cls.db.save_doc(current_doc, force_update=True)

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
            "channel": 1
        }
        self.notification_doc = {
            "collection": "notifications",
            "name": "Rob",
            "service": "phone",
            "user": "+447972058628",
            "status": "done"
        }
        res1 = self.db.save_doc(self.wifi_doc)
        self.test_doc_ids.append(res1['id'])
        dt = datetime.datetime(2015, 1, 5, hour=10, minute=5)
        self.hist1 = self.add_history_item(self.title, self.description, res1['id'], res1['rev'], 'wifi', 'edit', True, ts=dt.isoformat())
        self.test_doc_ids.append(self.hist1['id'])
        self.wifi_doc['ssid'] = 'testing2'
        res2 = self.db.save_doc(self.wifi_doc)
        dt = datetime.datetime(2015, 2, 5, hour=10, minute=5)
        self.hist2 = self.add_history_item(self.title, self.description, res2['id'], res2['rev'], 'wifi', 'edit', True, ts=dt.isoformat())
        self.test_doc_ids.append(self.hist2['id'])
        self.wifi_doc['ssid'] = 'testing3'
        res3 = self.db.save_doc(self.wifi_doc)
        dt = datetime.datetime(2015, 2, 23, hour=15, minute=0)
        self.hist3 = self.add_history_item(self.title, self.description, res3['id'], res3['rev'], 'wifi', 'edit', True, ts=dt.isoformat())
        self.test_doc_ids.append(self.hist3['id'])
        res4 = self.db.save_doc(self.notification_doc)
        self.test_doc_ids.append(res4['id'])
        self.notification_doc = self.db.get(res4['id'])
        notification_registration_client.registration(self.notification_doc)
        dt = datetime.datetime(2015, 2, 12, hour=14, minute=34)
        self.notification_doc = self.db.get(res4['id'])
        self.hist4 = self.add_history_item(self.title, self.description, res4['id'], self.notification_doc['_rev'], 'notifications', 'add', True, ts=dt.isoformat())
        self.test_doc_ids.append(self.hist4['id'])
        self.revert_timestamp = datetime.datetime(2015, 1, 20).isoformat()
        self.rb = perform_rollback.Rollback(self.db, {})

    def tearDown(self):
        for doc in self.test_doc_ids:
            opened = self.db.get(doc)
            opened['_deleted'] = True
            self.db.save_doc(opened, force_update=True)

    def add_history_item(self, title, description, docId, docRev, doc_collection, action='edit', undoable=True, ts=None):
        doc = {}
        doc['collection'] = 'events'
        doc['title'] = title
        doc['description'] = description
        doc['doc_collection'] = doc_collection
        doc['action'] = action
        if ts is None:
            doc['timestamp'] = datetime.datetime.now(tzutc()).isoformat()
        else:
            doc['timestamp'] = ts
        doc['doc_id'] = docId
        doc['doc_rev'] = docRev
        doc['undoable'] = undoable
        doc['perform_undo'] = False
        res = self.db.save_doc(doc)
        return res

    def test_process_rollback_get_events(self):
        result = self.rb.get_events_after_timestamp(self.revert_timestamp)
        result_list = list(result)
        self.assertEqual(3, len(result_list))

    def test_process_rollback_get_docs_to_revert(self):
        result = self.rb.get_docs_to_revert(self.revert_timestamp)
        self.assertEqual(2, len(result))
        k = result.keys()
        self.assertNotEqual(k[0], k[1])

    def test_rollback(self):
        result = self.rb.revert(self.revert_timestamp)
        self.assertTrue(result)
