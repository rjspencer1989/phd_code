import unittest
from process_config import CouchdbConfigParser, History


class TestHistory(unittest.TestCase):
    def test_history(self):
        result = History.addHistoryItem("Change WiFi", "Wifi Updated", "Rob", "aabbc", "2-33aabbcc", True)
        self.assertIsNotNone(result)
        db = CouchdbConfigParser.getDB()
        doc = db.get(result['id'])
        self.assertIsNotNone(doc)
        self.assertEqual(doc['collection'], 'events')
        self.assertIn('timestamp', doc)
        self.assertEqual("Change WiFi", doc['title'])
        self.assertEqual("Wifi Updated", doc['description'])
        self.assertEqual("Rob", doc['user'])
        self.assertEqual("aabbc", doc['doc_id'])
        self.assertEqual("2-33aabbcc", doc['doc_rev'])
        self.assertTrue(doc['undoable'])
        self.assertFalse(doc['perform_undo'])
        db.delete_doc(doc)
