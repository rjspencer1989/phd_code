import unittest
from process_config import couchdb_config_parser
from couchdbkit import *


class TestConfig(unittest.TestCase):
    def test_load_config(self):
        self.assertTrue(isinstance(CouchdbConfigParser.getDB(), Database))
