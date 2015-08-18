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
        res1 = cls.db.save_doc(cls.wifi_doc)
        cls.test_doc_ids.append(res1['id'])
        dt = datetime.datetime(2015, 1, 5, hour=10, minute=5)
        cls.hist1 = add_history.add_history_item(cls.title, cls.description, res1['id'], res1['rev'], 'wifi', 'edit', True, ts=dt.isoformat())
        cls.test_doc_ids.append(cls.hist1['id'])
        cls.wifi_doc['ssid'] = 'testing2'
        res2 = cls.db.save_doc(cls.wifi_doc)
        dt = datetime.datetime(2015, 2, 5, hour=10, minute=5)
        cls.hist2 = add_history.add_history_item(cls.title, cls.description, res2['id'], res2['rev'], 'wifi', 'edit', True, ts=dt.isoformat())
        cls.test_doc_ids.append(cls.hist2['id'])
        cls.wifi_doc['ssid'] = 'testing3'
        res3 = cls.db.save_doc(cls.wifi_doc)
        dt = datetime.datetime(2015, 2, 23, hour=15, minute=0)
        cls.hist3 = add_history.add_history_item(cls.title, cls.description, res3['id'], res3['rev'], 'wifi', 'edit', True, ts=dt.isoformat())
        cls.test_doc_ids.append(cls.hist3['id'])
        res4 = cls.db.save_doc(cls.notification_doc)
        cls.test_doc_ids.append(res4['id'])
        cls.notification_doc = cls.db.get(res4['id'])
        notification_registration_client.registration(cls.notification_doc)
        dt = datetime.datetime(2015, 2, 12, hour=14, minute=34)
        cls.notification_doc = cls.db.get(res4['id'])
        cls.hist4 = add_history.add_history_item(cls.title, cls.description, res4['id'], cls.notification_doc['_rev'], 'notifications', 'add', True, ts=dt.isoformat())
        cls.test_doc_ids.append(cls.hist4['id'])
        cls.revert_timestamp = datetime.datetime(2015, 1, 20).isoformat()
        cls.rb = perform_rollback.Rollback(cls.db, {})

    @classmethod
    def tearDownClass(cls):
        for doc in cls.test_doc_ids:
            opened = cls.db.get(doc)
            opened['_deleted'] = True
            cls.db.save_doc(opened, force_update=True)
        cls.db = None

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
