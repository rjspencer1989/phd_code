import unittest
from couchdbkit import *
from process_config import CouchdbConfigParser, NotificationRegistrationClient
import os


class TestNotificationRegistrationClient(unittest.TestCase):
    def setUp(self):
        doc = {
            "name" : "Rob",
            "service" : "twitter",
            "user" : "rjspencer1989",
            "collection" : "notifications",
            "status" : "pending"
        }

        self.db = CouchdbConfigParser.getDB()
        res = self.db.save_doc(doc)
        the_id = res['id']
        self.ret_doc = self.db.get(the_id)

    def tearDown(self):
        self.ret_doc = {}
        self.db = None

    def test_registration(self):
        self.assertIsNotNone(self.ret_doc)
        NotificationRegistrationClient.consumer.registration(self.ret_doc, os.environ['APP_ENGINE_ROUTER_ID'])
        added_doc = self.db.get(self.ret_doc['_id'])
        print added_doc
        assert('suid' in added_doc)

    def test_edit(self):
        self.assertIsNotNone(self.ret_doc)
        self.ret_doc['user'] = 'robjspencer'
        v2 = self.db.save_doc(self.ret_doc)
        NotificationRegistrationClient.consumer.edit(v2, os.environ['APP_ENGINE_ROUTER_ID'])
        added_doc = self.db.get(v2['_id'])
        print added_doc
        assert('suid' in added_doc)
