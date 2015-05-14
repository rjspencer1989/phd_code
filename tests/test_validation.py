import unittest
from process_config import CouchdbConfigParser


class TestValidation(unittest.TestCase):
    def test_no_collection(self):
        doc = {"foo": "bar"}
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_invalid_collection(self):
        doc = {
            "name":"Rob",
            "service":"email",
            "userdetails":"rob@robspencer.me.uk",
            "collection": "notify"
        }
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_notification_valid(self):
        doc = {
            "name" : "Rob",
            "service" : "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "pending"
        }
        db = CouchdbConfigParser.getDB()
        db.save_doc(doc)

    def test_notification_invalid_status(self):
        doc = {
            "name" : "Rob",
            "service" : "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "foo"
        }
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_notification_missing_name(self):
        doc = {
            "service" : "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "foo"
        }
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)
