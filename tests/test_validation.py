import unittest
from process_config import CouchdbConfigParser


class TestValidation(unittest.TestCase):
    def test_no_collection(self):
        doc = {"foo": "bar"}
        db = CouchdbConfigParser.getDB()
        db.save_doc(doc)
