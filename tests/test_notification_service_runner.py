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

        self.reg_result1 = self.db.save_doc(self.registration1)
        self.reg_result2 = self.db.save_doc(self.registration2)

    def tearDown(self):
        self.registration1['hidden'] = True
        self.db.save_doc(registration1, force_update=True)
        self.registration2['hidden'] = True
        self.db.save_doc(registration2, force_update=True)
        self.registration1 = {}
        self.registration2 = {}

    def test_get_user_names_no_match(self):
        doc = {
            "body": "test",
            "collection": "request_notification",
            "service": "phone",
            "status": "pending",
            "to": "Tom"
        }

        res = self.db.save_doc(doc)
        user_names = self.nsr.get_user_names(doc['to'], doc['service'])
        self.assertIsNone(user_names)
        self.db.delete_doc(res['id'])

    def test_get_user_names_single_name(self):
        doc = {
            "body": "test",
            "collection": "request_notification",
            "service": "phone",
            "status": "pending",
            "to": "Harry"
        }

        res = self.db.save_doc(doc)
        user_names = self.nsr.get_user_names(doc['to'], doc['service'])
        self.assertIsNotNone(user_names)
        user_names_lst = list(user_names)
        self.assertEqual(1, len(user_names_lst))
        self.assertEqual('Harry', user_names_lst[0]['key'][1])
        self.assertEqual('phone', user_names_lst[0]['key'][0])
        self.assertEqual('+447972058628', user_names_lst[0]['value'])
        self.db.delete_doc(res['id'])

    def test_get_user_names_everyone(self):
        doc = {
            "body": "test",
            "collection": "request_notification",
            "service": "phone",
            "status": "pending",
            "to": "everyone"
        }

        res = self.db.save_doc(doc)
        user_names = self.nsr.get_user_names(doc['to'], doc['service'])
        self.assertIsNotNone(user_names)
        user_names_lst = list(user_names)
        self.assertEqual(2, len(user_names_lst))
        self.assertEqual('Harry', user_names_lst[0]['key'][1])
        self.assertEqual('Rob', user_names_lst[1]['key'][1])
        doc['hidden'] = True
        self.db.save_doc(doc, force_update=True)

    # @unittest.skip("stop the spam")
    def test_send_notification(self):
        doc = {
            "body": "test",
            "collection": "request_notification",
            "service": "phone",
            "status": "pending",
            "to": "Harry"
        }

        res = self.db.save_doc(doc)
        result = self.nsr.send_notification(res['id'], doc['to'], doc['service'], '+447972058628', doc['body'])
        self.assertTrue(result)
        self.db.delete_doc(res['id'])

    # @unittest.skip("stop the spam")
    def test_process_notification(self):
        doc = {
            "body": "test",
            "collection": "request_notification",
            "service": "phone",
            "status": "pending",
            "to": "Harry"
        }

        res = self.db.save_doc(doc)
        self.nsr.process_notification(doc)
        updated = self.db.open_doc(res['id'])
        self.assertEqual('done', updated['status'])
        self.db.delete_doc(res['id'])
