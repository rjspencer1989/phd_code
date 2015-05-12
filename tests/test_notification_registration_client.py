import unittest
from couchdbkit import *
from process_config import CouchdbConfigParser, NotificationRegistrationClient


class TestNotificationRegistrationClient(unittest.TestCase):
    def test_registration(self):
        doc = {
            "name" : "Rob",
            "service" : "twitter",
            "user" : "rjspencer1989",
            "collection" : "notifications",
            "status" : "pending"
        }

        db = CouchdbConfigParser.getDB()
        res = db.save_doc(doc)
        the_id = res['id']
        self.assertIsNotNone(the_id)
