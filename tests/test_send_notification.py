import unittest
from couchdbkit import *
from process_config import ChangeNotification, CouchdbConfigParser


class TestSendNotification(unittest.TestCase):
    def test_send_notification(self):
        res = ChangeNotification.sendNotification("Rob", "email", "foo")
        db = CouchdbConfigParser.getDB()
        ret_doc = db.get(res)
        print ret_doc
        self.assertTrue(ret_doc is not None)
