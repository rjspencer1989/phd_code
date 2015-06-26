import unittest
from couchdbkit import *
from process_config import couchdb_config_parser
from process_config import notification_registration_client
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

        self.db = couchdb_config_parser.get_db()
        res = self.db.save_doc(doc)
        self.the_id = res['id']
        self.ret_doc = self.db.get(self.the_id)

    def tearDown(self):
        self.ret_doc['hidden'] = True
        self.db.save_doc(self.ret_doc, force_update=True)
        self.ret_doc = {}
        self.db = None

    def test_registration(self):
        self.assertIsNotNone(self.ret_doc)
        notification_registration_client.registration(self.ret_doc)
        added_doc = self.db.get(self.the_id)
        self.assertIn('suid', added_doc)

    def test_edit(self):
        self.assertIsNotNone(self.ret_doc)
        notification_registration_client.registration(self.ret_doc)
        added_doc = self.db.get(self.the_id)
        added_doc['user'] = 'robjspencer'
        res = self.db.save_doc(added_doc)
        v2 = self.db.get(self.the_id)
        notification_registration_client.edit(v2)
        added_doc = self.db.get(self.the_id)
        self.assertIn('suid', added_doc)

    def test_delete(self):
        self.assertIsNotNone(self.ret_doc)
        notification_registration_client.registration(self.ret_doc)
        v2 = self.db.get(self.the_id)
        notification_registration_client.delete(v2)
        added_doc = self.db.get(self.the_id)
        self.assertEqual(added_doc['suid'], '')
        self.assertEqual(added_doc['status'], 'done')
