import unittest
from process_config import CouchdbConfigParser


class TestConfig(unittest.TestCase):
    def testLoadConfig(self):
        assertTrue(CouchdbConfigParser.getDB() is not None)
if __name__ == '__main__':
    unittest.main()
