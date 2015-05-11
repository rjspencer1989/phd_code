import unittest
from couchdbkit import *
from process_config import ChangeNotification, CouchdbConfigParser


class TestSendNotification(unittest.TestCase):
    def test_send_notification(self):
        the_id = ''
        res = ChangeNotification.sendNotification("Rob", "email", "foo")
        the_id = res['id']
        db = CouchdbConfigParser.getDB()
        ret_doc = db.get(the_id)
        print ret_doc
        self.assertEqual(ret_doc['_id'], the_id)
        self.assertEqual(ret_doc['collection'], 'notification-request')
        self.assertEqual(ret_doc['status'], 'pending')
        self.assertEqual(ret_doc['to'], 'Rob')
        self.assertEqual(ret_doc['service'], 'email')
        self.assertEqual(ret_doc['body'], 'foo')
