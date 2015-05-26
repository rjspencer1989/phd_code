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

    def tearDown(self):
        for doc in self.test_doc_ids:
            self.db.delete_doc(doc)

    def test_process_rollback(self):
        doc1 = {
            "collection": "wifi",
            "status": "done",
            "ssid": "testing",
            "mode": "g",
            "encryption_type": "wep",
            "password_type": "txt",
            "password": "whatever12345",
            "channel": 1
        }
        res1 = self.db.save_doc(doc1)
        self.test_doc_ids.append(res1['id'])
        dt = datetime.datetime(2015, 1, 5, hour=10, minute=5)
        hist1 = self.add_history_item(res1['id'], res1['rev'], dt.isoformat())
        self.test_doc_ids.append(hist1['id'])
        doc1['ssid'] = 'testing2'
        res2 = self.db.save_doc(doc1)
        dt = datetime.datetime(2015, 2, 5, hour=10, minute=5)
        hist2 = self.add_history_item(res2['id'], res2['rev'], dt.isoformat())
        self.test_doc_ids.append(hist2['id'])
        doc1['ssid'] = 'testing3'
        res3 = self.db.save_doc(doc1)
        dt = datetime.datetime(2015, 2, 23, hour=15, minute=0)
        hist3 = self.add_history_item(res3['id'], res3['rev'], dt.isoformat())
        self.test_doc_ids.append(hist3['id'])
        result = perform_rollback.perform_rollback(datetime.datetime(2015, 1, 20).isoformat())
        print result
        result_list = list(result)
        self.assertEqual(2, len(result_list))

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
