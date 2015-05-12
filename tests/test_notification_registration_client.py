import unittest
from couchdbkit import *
from process_config import CouchdbConfigParser, NotificationRegistrationClient


class TestNotificationRegistrationClient(unittest.TestCase):
    def test_registration(self):
        name = "Rob"
        service = "twitter"
