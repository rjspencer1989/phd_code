import unittest
from couchdbkit import *
from process_config import ChangeNotification


class TestSendNotification(unittest.TestCase):
    def test_send_notification(self):
        res = ChangeNotification.sendNotification("Rob", "email", "foo")
        self.assertTrue(res is not None)
