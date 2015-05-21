import unittest
from process_config import couchdb_config_parser, perform_undo, add_history
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
        db = couchdb_config_parser.getDB()
        res = db.save_doc(nd)
        event_res = History.add_history_item("new notification", "added notification mapping for Rob using Twitter and username rjspencer1989", "Rob", res['id'], res['rev'], True)
        event = db.get(event_res['id'])
        doc = undo_consumer.get_doc_to_undo(event)
        rev_list = undo_consumer.get_rev_list(doc, res['rev'])
        result = undo_consumer.undo(doc, rev_list)
        updated = db.get(nd['_id'], rev=result)
        self.assertTrue('_deleted' in updated)
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
        db = couchdb_config_parser.getDB()
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
            "action": "",
            "collection": "devices",
            "device_name": "",
            "host_name": "test-device",
            "ip_address": "10.2.0.61",
            "lease_action": "add",
            "mac_address": "aa:bb:cc:dd:ee:ff",
            "name": "",
            "state": "pending",
            "device_type": "",
            "notification_service": "",
            "timestamp": time.time(),
            "connected": True,
            "changed_by": "system"
        }
        db = couchdb_config_parser.getDB()
        db.save_doc(doc)  # initial from DHCP
        doc['action'] = 'deny'
        doc['device_name'] = 'test-device'
        doc['name'] = 'Rob'
        doc['device_type'] = 'laptop'
        doc['notification_service'] = 'phone'
        doc['changed_by'] = 'user'
        db.save_doc(doc)  # initial user decision
        doc['action'] = ''
        doc['state'] = 'deny'
        doc['changed_by'] = 'system'
        db.save_doc(doc)  # POX applying change
        doc['action'] = 'permit'
        doc['changed_by'] = 'user'
        res = db.save_doc(doc)  # user changes their mind
        event_res = History.add_history_item("Permit device", "Permitted  test-device", "Rob", res['id'], res['rev'], True)
        event = db.get(event_res['id'])
        undo_doc = undo_consumer.get_doc_to_undo(event)
        result = undo_consumer.undo_device_change(undo_doc, res['rev'])
        updated = db.open_doc(doc['_id'], rev=result)
        self.assertEqual('deny', updated['action'])
        db.delete_doc(event_res['id'])
        db.delete_doc(doc['_id'])
