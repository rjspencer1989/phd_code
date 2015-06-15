import unittest
from process_config import couchdb_config_parser, add_history, notification_registration_client
from undo import perform_undo
from undo.doc_types import notifications
import time


class TestPerformUndo(unittest.TestCase):
    def test_process_undo_notification_new_doc(self):
        undo_consumer = perform_undo.consumer
        nd = {
            "collection": "notifications",
            "status": "done",
            "name": "Rob",
            "service": "twitter",
            "user": "rjspencer1989"
        }
        db = couchdb_config_parser.get_db()
        res = db.save_doc(nd)
        notification_registration_client.registration(nd)
        nd = db.get(nd)
        event_res = add_history.add_history_item("new notification", "added notification mapping for Rob using Twitter and username rjspencer1989", res['id'], res['rev'], True)
        event = db.get(event_res['id'])
        result = undo_consumer.perform_undo(event)
        updated = db.get(nd['_id'], rev=result)
        self.assertTrue('hidden' in updated)
        event['_deleted'] = True
        db.save_doc(event, force_update=True)
    #
    # def test_process_undo_notification_existing_doc(self):
    #     undo_consumer = perform_undo.consumer
    #     nd = {
    #         "collection": "notifications",
    #         "status": "done",
    #         "name": "Rob",
    #         "service": "twitter",
    #         "user": "rjspencer1989"
    #     }
    #     db = couchdb_config_parser.get_db()
    #     res = db.save_doc(nd)
    #     nd['user'] = 'robjspencer'
    #     res2 = db.save_doc(nd)
    #     event_res = add_history.add_history_item("edit notification", "Edited notification mapping for Rob using Twitter and username robjspencer", res2['id'], res2['rev'], True)
    #     event = db.get(event_res['id'])
    #     doc = undo_consumer.get_doc_to_undo(event)
    #     rev_list = undo_consumer.get_rev_list(doc, res2['rev'])
    #     result = undo_consumer.undo(doc, rev_list)
    #     updated = db.get(nd['_id'], rev=result)
    #     self.assertEqual(updated['user'], 'rjspencer1989')
    #     nd['hidden'] = True
    #     db.save_doc(nd, force_update=True)
    #     event['_deleted'] = True
    #     db.save_doc(event, force_update=True)
    #
    # def test_process_undo_device_doc(self):
    #     undo_consumer = perform_undo.consumer
    #     doc = {
    #         "_id": "11:aa:33:bb:cc:ff",
    #         "action": "",
    #         "collection": "devices",
    #         "device_name": "",
    #         "host_name": "test-device",
    #         "ip_address": "10.2.0.61",
    #         "lease_action": "add",
    #         "mac_address": "11:aa:33:bb:cc:ff",
    #         "name": "",
    #         "state": "pending",
    #         "device_type": "",
    #         "notification_service": "",
    #         "timestamp": time.time(),
    #         "connection_event": "connect",
    #         "changed_by": "system"
    #     }
    #     db = couchdb_config_parser.get_db()
    #     db.save_doc(doc)  # initial from DHCP
    #     doc['action'] = 'deny'
    #     doc['device_name'] = 'test-device'
    #     doc['name'] = 'Rob'
    #     doc['device_type'] = 'laptop'
    #     doc['notification_service'] = 'phone'
    #     doc['changed_by'] = 'user'
    #     db.save_doc(doc)  # initial user decision
    #     doc['action'] = ''
    #     doc['state'] = 'deny'
    #     doc['changed_by'] = 'system'
    #     db.save_doc(doc)  # POX applying change
    #     doc['action'] = 'permit'
    #     doc['changed_by'] = 'user'
    #     res = db.save_doc(doc)  # user changes their mind
    #     event_res = add_history.add_history_item("Permit device", "Permitted  test-device", res['id'], res['rev'], True)
    #     event = db.get(event_res['id'])
    #     undo_doc = undo_consumer.get_doc_to_undo(event)
    #     result = undo_consumer.undo_device_change(undo_doc, res['rev'])
    #     updated = db.open_doc(doc['_id'], rev=result)
    #     self.assertEqual('deny', updated['action'])
    #     event['_deleted'] = True
    #     doc['_deleted'] = True
    #     db.save_doc(doc, force_update=True)
    #     db.save_doc(event, force_update=True)
