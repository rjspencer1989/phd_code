import unittest
from process_config import CouchdbConfigParser
import couchdbkit.exceptions


class TestValidation(unittest.TestCase):
    def test_no_collection(self):
        doc = {"foo": "bar"}
        db = CouchdbConfigParser.getDB()
        self.assertRaises(Exception, db.save_doc(doc))

    def test_invalid_collection(self):
        doc = {"name":"Rob", "service":"email", "userdetails":"rob@robspencer.me.uk", "collection": "notify"}
        db = CouchdbConfigParser.getDB()
        self.assertRaises(Exception, db.save_doc(doc))
