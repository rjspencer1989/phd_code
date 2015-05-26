import unittest
from process_config import couchdb_config_parser, perform_rollback, add_history
import datetime
import mock


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
        self.rb = perform_rollback.Rollback(datetime.datetime(2015, 1, 20).isoformat())

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
        result = self.rb.get_events_after_timestamp()
        result_list = list(result)
        self.assertEqual(2, len(result_list))

    def test_process_rollback_get_doc(self):
        hist_doc = self.db.get(self.hist1['id'], rev=self.hist1['rev'])
        result = self.rb.get_doc_for_event(hist_doc)
        self.assertEqual('testing', result['ssid'])

    def test_process_rollback_get_docs_to_revert(self):
        self.maxDiff = None
        result = self.rb.get_docs_to_revert()
        self.assertEqual(1, len(result))
