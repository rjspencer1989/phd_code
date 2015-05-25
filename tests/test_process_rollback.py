import unittest
from process_config import couchdb_config_parser, perform_rollback, add_history
import time
import mock


class TestProcessRollback(unittest.TestCase):
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
        db = couchdb_config_parser.get_db()
        res1 = db.save_doc(doc1)
        hist1 = add_history.add_history_item("edit wifi", "edit wifi", "Rob", res1['id'], res1['rev'], True)
        timestamp = time.time() - 20
        result = perform_rollback.perform_rollback(timestamp)
        db.delete_doc(res1['id'])
        db.delete_doc(hist1['id'])

    def addHistoryItem(doc_id, doc_rev, timestamp):
        doc = {
            'collection': 'events',
            'title': 'rollback test',
            'description': 'rollback description',
            'timestamp': timestamp,
            'doc_id': doc_id,
            'doc_rev': doc_rev,
            'undoable': True,
            'perform_undo': False
        }

        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc)
        return res
