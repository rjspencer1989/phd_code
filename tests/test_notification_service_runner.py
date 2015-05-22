import unittest
from notifications import notification_service_runner
from process_config import couchdb_config_parser


class TestNotificationServiceRunner(unittest.TestCase):
    def test_get_user_names(self):
        nsr = notification_service_runner.notification_consumer
        doc = {
            "body": "test",
            "collection": "notification-request",
            "service": "phone",
            "status": "pending",
            "to": "Rob"
        }

        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc)
        user_names = nsr.get_user_names(doc['to'], doc['service'])
        print user_names
        db.delete_doc(res['id'])
