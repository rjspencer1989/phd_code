import unittest
from process_config import CouchdbConfigParser, Undo, History
import time


class TestProcessUndo(unittest.TestCase):
    def test_process_undo_new_doc(self):
        undo_consumer = Undo.consumer
        nd = {
            "collection": "notifications",
            "status": "done",
            "name": "Rob",
            "service": "twitter",
            "user": "rjspencer1989"
        }
        db = CouchdbConfigParser.getDB()
        res = db.save_doc(nd)
        event_res = History.add_history_item("new notification", "added notification mapping for Rob using Twitter and username rjspencer1989", "Rob", res['id'], res['rev'], True)
        event = db.get(event_res['id'])
        doc = undo_consumer.get_doc_to_undo(event)
        rev_list = undo_consumer.get_rev_list(doc, res['rev'])
        result = undo_consumer.undo(doc, rev_list)
        self.assertTrue('_deleted' in nd)
        db.delete_doc(event_res['id'])

    def test_process_undo_existing_doc(self):
        undo_consumer = Undo.consumer
        nd = {
            "collection": "notifications",
            "status": "done",
            "name": "Rob",
            "service": "twitter",
            "user": "rjspencer1989"
        }
        db = CouchdbConfigParser.getDB()
        res = db.save_doc(nd)
        nd['user'] = 'robjspencer'
        res2 = db.save_doc(nd)
        event_res = History.add_history_item("edit notification", "Edited notification mapping for Rob using Twitter and username robjspencer", "Rob", res2['id'], res2['rev'], True)
        event = db.get(event_res['id'])
        doc = undo_consumer.get_doc_to_undo(event)
        rev_list = undo_consumer.get_rev_list(doc, res2['rev'])
        result = undo_consumer.undo(doc, rev_list)
        updated = db.get(nd['_id'], rev=result)
        self.assertEqual(updated['user'], 'rjspencer1989')
        db.delete_doc(res['id'])
        db.delete_doc(event_res['id'])

    def test_process_undo_device_doc(self):
        undo_consumer = Undo.consumer
        doc = {
            "_id": "aa:bb:cc:dd:ee:ff",
            "action": "permit",
            "collection": "devices",
            "device_name": "test-device",
            "host_name": "test-device",
            "ip_address": "10.2.0.61",
            "lease_action": "add",
            "mac_address": "aa:bb:cc:dd:ee:ff",
            "name": "Rob",
            "state": "pending",
            "device_type": "laptop",
            "notification_service": "email",
            "timestamp": time.time(),
            "connected": False,
            "changed_by": "user"
        }
        db = CouchdbConfigParser.getDB()
        db.save_doc(doc)  # initial from DHCP
        db.save_doc(doc)  # initial user decision
        db.save_doc(doc)  # POX applying change
        res = db.save_doc(doc)  # user changes their mind
        event_res = History.add_history_item("Permit device", "Permitted  test-device", "Rob", res['id'], res['rev'], True)
        event = db.get(event_res['id'])
        undo_doc = undo_consumer.get_doc_to_undo(event)
        result = undo_consumer.undo_device_change(undo_doc, res['rev'])
        db.delete_doc(event_res['id'])
        db.delete_doc(doc['_id'])
