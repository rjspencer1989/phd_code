import unittest
from notifications import notification_service_runner
from process_config import couchdb_config_parser


class TestNotificationServiceRunner(unittest.TestCase):
    def test_process_notification(self):
        doc = {
            "body": "test",
            "collection": "notification-request",
            "service": "phone",

        }
