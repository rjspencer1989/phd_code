import unittest
from process_config import CouchdbConfigParser, History


class TestHistory(unittest.TestCase):
    def testHistory(self):
        result = History.addHistoryItem("Change WiFi", "Wifi Updated", "Rob", "aabbc", "2-33aabbcc", True)
        self.assertIsNotNone(result)
        db = CouchdbConfigParser.getDB()
        doc = db.get(result['id'])
        self.assertIsNotNone(doc)
        self.assertEqual(doc['collection'], 'event')
        self.assertIn('timestamp', doc)
        self.assertEqual("Change WiFi", doc['title'])
        self.assertEqual("Wifi Updated", doc['description'])
        self.assertEqual("Rob", doc['user'])
        self.assertEqual("aabbc", doc['doc_id'])
        self.assertEqual("2-33aabbbcc", doc['doc_rev'])
        self.assertTrue(doc['undoable'])
        self.assertFalse(doc['process_undo'])
