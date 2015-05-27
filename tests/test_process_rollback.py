import unittest
from process_config import couchdb_config_parser, perform_rollback, add_history
import datetime
import mock
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
        self.db = couchdb_config_parser.get_db()
        self.wifi_doc = {
            "collection": "wifi",
            "status": "done",
            "ssid": "testing",
            "mode": "g",
            "encryption_type": "wep",
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
        self.hist1 = self.add_history_item(res1['id'], res1['rev'], dt.isoformat())
        self.test_doc_ids.append(self.hist1['id'])
        self.wifi_doc['ssid'] = 'testing2'
        res2 = self.db.save_doc(self.wifi_doc)
        dt = datetime.datetime(2015, 2, 5, hour=10, minute=5)
        self.hist2 = self.add_history_item(res2['id'], res2['rev'], dt.isoformat())
        self.test_doc_ids.append(self.hist2['id'])
        self.wifi_doc['ssid'] = 'testing3'
        res3 = self.db.save_doc(self.wifi_doc)
        dt = datetime.datetime(2015, 2, 23, hour=15, minute=0)
        self.hist3 = self.add_history_item(res3['id'], res3['rev'], dt.isoformat())
        self.test_doc_ids.append(self.hist3['id'])
        res4 = self.db.save_doc(self.notification_doc)
        self.test_doc_ids.append(res4['id'])
        dt = datetime.datetime(2015, 2, 12, hour=14, minute=34)
        self.hist4 = self.add_history_item(res4['id'], res4['rev'], dt.isoformat())
        self.test_doc_ids.append(self.hist4['id'])
        self.revert_timestamp = datetime.datetime(2015, 1, 20).isoformat()
        self.rb = perform_rollback.consumer

    def tearDown(self):
        for doc in self.test_doc_ids:
            self.db.delete_doc(doc)

    def add_history_item(self, doc_id, doc_rev, timestamp):
        doc = {
            'collection': 'events',
            'title': 'rollback test',
            'description': 'rollback description',
            'timestamp': timestamp,
            'doc_id': doc_id,
            'doc_rev': doc_rev,
            'undoable': True,
            'perform_undo': False,
            'user': 'travis_ci'
        }

        res = self.db.save_doc(doc)
        return res

    def test_process_rollback_get_events(self):
        result = self.rb.get_events_after_timestamp(self.revert_timestamp)
        result_list = list(result)
        self.assertEqual(3, len(result_list))

    def test_process_rollback_get_docs_to_revert(self):
        result = self.rb.get_docs_to_revert(self.revert_timestamp)
        pprint.pprint(result)
        self.assertEqual(2, len(result))
        k = result.keys()
        self.assertNotEqual(k[0], k[1])

    def test_rollback(self):
        result = self.rb.revert(self.revert_timestamp)
        hist_docs = [self.hist1, self.hist2, self.hist3, self.hist4]
        for doc in hist_docs:
            pprint.pprint(doc)
