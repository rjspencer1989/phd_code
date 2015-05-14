import unittest
from process_config import CouchdbConfigParser
from couchdbkit import *


class TestConfig(unittest.TestCase):
    def test_load_config(self):
        self.assertTrue(isinstance(CouchdbConfigParser.getDB(), Database))
