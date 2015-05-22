import unittest
from notifications import notification_service_runner
from process_config import couchdb_config_parser


class TestNotificationServiceRunner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nsr = notification_service_runner.notification_consumer
        cls.db = couchdb_config_parser.get_db()

    @classmethod
    def tearDownClass(cls):
        cls.nsr = None
        cls.db = None

    def setUp(self):
        self.registration1 = {
            "collection": "notifications",
            "name": "Rob",
            "service": "phone",
            "user": "+447972058628",
            "status": "done"
        }

        self.registration2 = {
            "collection": "notifications",
            "name": "Harry",
            "service": "phone",
            "user": "+447972058628",
            "status": "done"
        }

        self.reg_result1 = db.save_doc(self.registration1)
        self.reg_result2 = db.save_doc(self.registration2)

    def tearDown(self):
        db.delete_doc(self.reg_result['id'])
        self.registration1 = {}
        self.registration2 = {}

    def test_get_user_names_no_match(self):
        doc = {
            "body": "test",
            "collection": "notification-request",
            "service": "phone",
            "status": "pending",
            "to": "Tom"
        }

        db = couchdb_config_parser.get_db()
        res = db.save_doc(doc)
        user_names = nsr.get_user_names(doc['to'], doc['service'])
        self.assertIsNone(user_names)
        db.delete_doc(res['id'])
