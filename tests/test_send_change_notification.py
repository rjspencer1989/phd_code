import unittest
from couchdbkit import *
from process_config import change_notification, couchdb_config_parser


class TestSendNotification(unittest.TestCase):
    def test_send_notification(self):
        the_id = ''
        res = change_notification.sendNotification("Rob", "email", "foo")
        the_id = res['id']
        db = couchdb_config_parser.get_db()
        ret_doc = db.get(the_id)
        self.assertEqual(ret_doc['_id'], the_id)
        self.assertEqual(ret_doc['collection'], 'request_notification')
        self.assertEqual(ret_doc['status'], 'pending')
        self.assertEqual(ret_doc['to'], 'Rob')
        self.assertEqual(ret_doc['service'], 'email')
        self.assertEqual(ret_doc['body'], 'foo')
        ret_doc['hidden'] = True
        db.save_doc(ret_doc, force_update=True)
