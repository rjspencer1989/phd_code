import unittest
from couchdbkit import *
from process_config import CouchdbConfigParser, NotificationRegistrationClient
import os


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
        ret_doc = db.get(the_id)
        self.assertIsNotNone(ret_doc)
        NotificationRegistrationClient.consumer.registration(ret_doc, os.environ['APP_ENGINE_ROUTER_ID'])
        added_doc = db.get(the_id)
        print added_doc
        assert('suid' in added_doc)
