import unittest
from process_config import CouchdbConfigParser
import urllib2


class TestValidation(unittest.TestCase):
    def test_no_collection(self):
        doc = {"foo": "bar"}
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(urllib2.HTTPError):
            db.save_doc(doc)
