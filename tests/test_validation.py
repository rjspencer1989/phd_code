import unittest
from process_config import CouchdbConfigParser
import couchdbkit


class TestValidation(unittest.TestCase):
    def test_no_collection(self):
        doc = {"foo": "bar"}
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(couchdbkit.BadValueError):
            db.save_doc(doc)