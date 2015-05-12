import unittest
from process_config import CouchdbConfigParser, History


class TestHistory(unittest.TestCase):
    def testHistory(self):
        result = History.addHistoryItem("Change WiFi", "Wifi Updated", "Rob", "aabbc", "2-33aabbcc", True)
        self.assertIsNotNone(result)
