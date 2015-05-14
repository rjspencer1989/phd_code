import unittest
from process_config import CouchdbConfigParser
import couchdbkit.exceptions


class TestValidation(unittest.TestCase):
    def test_no_collection(self):
        doc = {"foo": "bar"}
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(couchdbkit.exceptions.BadValueError):
            db.save_doc(doc)
