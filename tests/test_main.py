import unittest
from process_config import CouchdbConfigParser


class TestConfig(unittest.TestCase):
    def test_LoadConfig(self):
        self.assertTrue(CouchdbConfigParser.getDB() is not None)
