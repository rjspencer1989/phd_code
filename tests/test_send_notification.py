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
        self.assertTrue(ret_doc is not None)
