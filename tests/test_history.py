import unittest
from process_config import add_history, couchdb_config_parser


class TestHistory(unittest.TestCase):
    def test_history(self):
        result = add_history.add_history_item("Change WiFi",
                                              "Wifi Updated",
                                              "aabbc",
                                              "2-33aabbcc", "wifi", "edit", True)
        self.assertIsNotNone(result)
        db = couchdb_config_parser.get_db()
        doc = db.get(result['id'])
        self.assertIsNotNone(doc)
        self.assertEqual(doc['collection'], 'events')
        self.assertIn('timestamp', doc)
        self.assertEqual("Change WiFi", doc['title'])
        self.assertEqual("Wifi Updated", doc['description'])
        self.assertEqual("aabbc", doc['doc_id'])
        self.assertEqual("2-33aabbcc", doc['doc_rev'])
        self.assertTrue(doc['undoable'])
        self.assertFalse(doc['perform_undo'])
        doc['_deleted'] = True
        db.save_doc(doc)
