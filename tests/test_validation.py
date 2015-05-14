import unittest
from process_config import CouchdbConfigParser
import datetime


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

    def test_required(self):
        doc = {
            "service" : "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "foo"
        }
        db = CouchdbConfigParser.getDB()
        with self.assertRaises(Exception):
            db.save_doc(doc)

    def test_unchanged(self):
        doc = {
            "name" : "Rob",
            "service" : "twitter",
            "collection": "notifications",
            "user": "rjspencer1989",
            "status": "pending"
        }
        db = CouchdbConfigParser.getDB()
        db.save_doc(doc)
        doc['name'] = 'test'
        with self.assertRaises(Exception):
            db.save_doc(doc, force_update=True)

    def test_event(self):
        doc = {
            "timestamp" : datetime.datetime.now().isoformat(),
            "collection": "events",
            "title": "testing",
            "description": "testing, testing, 1,2,3",
            "user": "Rob",
            "doc_id": "aabbcc",
            "doc_rev": "1-aabbcc",
            "undoable": True,
            "perform_undo": False
        }
        db = CouchdbConfigParser.getDB()
        db.save_doc(doc)
