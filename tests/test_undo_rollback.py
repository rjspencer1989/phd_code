import unittest
from process_config import couchdb_config_parser, perform_rollback, notification_registration_client
from process_config.add_history import add_history_item
from undo import perform_undo
from undo.doc_types import request_revert
import time
import pprint
import datetime


class TestUndoRollback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = couchdb_config_parser.get_db()
        current_events = cls.db.view('homework-remote/events')
        if current_events.count() > 0:
            current_events_all = current_events.all()
            for row in current_events_all:
                current_doc = cls.db.get(row['id'])
                current_doc['_deleted'] = True
                cls.db.save_doc(current_doc, force_update=True)

        self.test_doc_ids = []
        self.title = "test rollback"
        self.description = "test rollback description"
        self.wifi_doc = {
            "collection": "wifi",
            "status": "done",
            "ssid": "testing",
            "mode": "g",
            "encryption_type": "wpa",
            "password_type": "txt",
            "password": "whatever12345",
            "channel": 1
        }
        self.notification_doc = {
            "collection": "notifications",
            "name": "Rob",
            "service": "phone",
            "user": "+447972058628",
            "status": "done"
        }
        self.revert_doc = {
            "collection": "request_revert",
            "timestamp": datetime.datetime(2015, 1, 20).isoformat(),
            "status": "pending"
        }
        res1 = self.db.save_doc(self.wifi_doc)
        self.test_doc_ids.append(res1['id'])
        dt = datetime.datetime(2015, 1, 5, hour=10, minute=5)
        self.hist1 = self.add_history_item(self.title, self.description, res1['id'], res1['rev'], 'wifi', 'edit', True, ts=dt.isoformat())
        self.test_doc_ids.append(self.hist1['id'])
        self.wifi_doc['ssid'] = 'testing2'
        res2 = self.db.save_doc(self.wifi_doc)
        dt = datetime.datetime(2015, 2, 5, hour=10, minute=5)
        self.hist2 = self.add_history_item(self.title, self.description, res2['id'], res2['rev'], 'wifi', 'edit', True, ts=dt.isoformat())
        self.test_doc_ids.append(self.hist2['id'])
        self.wifi_doc['ssid'] = 'testing3'
        res3 = self.db.save_doc(self.wifi_doc)
        dt = datetime.datetime(2015, 2, 23, hour=15, minute=0)
        self.hist3 = self.add_history_item(self.title, self.description, res3['id'], res3['rev'], 'wifi', 'edit', True, ts=dt.isoformat())
        self.test_doc_ids.append(self.hist3['id'])
        res4 = self.db.save_doc(self.notification_doc)
        self.notification_doc = self.db.get(res4['id'])
        notification_registration_client.registration(self.notification_doc)
        self.test_doc_ids.append(res4['id'])
        self.revert_res = self.db.save_doc(self.revert_doc)
        self.revert_doc = self.db.get(self.revert_res['id'])
        self.test_doc_ids.append(self.revert_res['id'])
        self.notification_doc = self.db.get(self.notification_doc['_id'])
        dt = datetime.datetime(2015, 2, 12, hour=14, minute=34)
        self.hist4 = self.add_history_item(self.title, self.description, self.notification_doc['_id'], self.notification_doc['_rev'], 'notifications', 'add', True, ts=dt.isoformat())
        self.test_doc_ids.append(self.hist4['id'])
        pprint.pprint(self.notification_doc)
        self.rb = perform_rollback.Rollback(self.db, self.revert_doc)
        self.rb.revert(self.revert_doc['timestamp'])
        rd = self.db.get(self.revert_doc['_id'], revs_info=True)
        dt = datetime.datetime(2015, 7, 23, hour=15, minute=0)
        self.rd_hist = self.add_history_item("unrev", "unrev", rd['_id'], rd['_rev'], 'request_revert', ts=dt.isoformat())
        self.test_doc_ids.append(self.rd_hist['id'])
        self.undo_revert = request_revert.Request_revert(rd, self.db.get(self.rd_hist['id']))

    @classmethod
    def tearDownClass(cls):
        for doc in self.test_doc_ids:
            opened = self.db.get(doc)
            opened['_deleted'] = True
            self.db.save_doc(opened, force_update=True)
        cls.db = None

    def add_history_item(self, title, description, docId, docRev, doc_collection, action='edit', undoable=True, ts=None):
        doc = {}
        doc['collection'] = 'events'
        doc['title'] = title
        doc['description'] = description
        doc['doc_collection'] = doc_collection
        doc['action'] = action
        if ts is None:
            doc['timestamp'] = datetime.datetime.now(tzutc()).isoformat()
        else:
            doc['timestamp'] = ts
        doc['doc_id'] = docId
        doc['doc_rev'] = docRev
        doc['undoable'] = undoable
        doc['perform_undo'] = False
        res = self.db.save_doc(doc)
        return res

    def test_get_events(self):
        result = self.undo_revert.get_events(self.revert_doc['timestamp'])
        vra = result.all()
        pprint.pprint(vra)
        self.assertEqual(4, result.count())

    def test_get_reverted_events(self):
        result = self.undo_revert.get_reverted_events()
        pprint.pprint(result)
