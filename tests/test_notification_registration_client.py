import unittest
from couchdbkit import *
from process_config import CouchdbConfigParser, NotificationRegistrationClient
import os


class TestNotificationRegistrationClient(unittest.TestCase):
    def setUp(self):
        doc = {
            "name": "Rob",
            "service": "twitter",
            "user": "rjspencer1989",
            "collection": "notifications",
            "status": "pending"
        }

        self.db = CouchdbConfigParser.getDB()
        res = self.db.save_doc(doc)
        self.the_id = res['id']
        self.ret_doc = self.db.get(self.the_id)

    def tearDown(self):
        self.db.delete_doc(self.the_id)
        self.ret_doc = {}
        self.db = None

    def test_registration(self):
        self.assertIsNotNone(self.ret_doc)
        NotificationRegistrationClient.consumer.registration(self.ret_doc, os.environ['APP_ENGINE_ROUTER_ID'])
        added_doc = self.db.get(self.the_id)
        assert('suid' in added_doc)

    def test_edit(self):
        self.assertIsNotNone(self.ret_doc)
        NotificationRegistrationClient.consumer.registration(self.ret_doc, os.environ['APP_ENGINE_ROUTER_ID'])
        added_doc = self.db.get(self.the_id)
        added_doc['user'] = 'robjspencer'
        res = self.db.save_doc(added_doc)
        v2 = self.db.get(self.the_id)
        NotificationRegistrationClient.consumer.edit(v2, os.environ['APP_ENGINE_ROUTER_ID'])
        added_doc = self.db.get(self.the_id)
        assert('suid' in added_doc)

    def test_delete(self):
        self.assertIsNotNone(self.ret_doc)
        NotificationRegistrationClient.consumer.registration(self.ret_doc, os.environ['APP_ENGINE_ROUTER_ID'])
        added_doc = self.db.get(self.the_id)
        code = NotificationRegistrationClient.consumer.delete(added_doc, os.environ['APP_ENGINE_ROUTER_ID'])
        self.assertEqual(code, 200)
