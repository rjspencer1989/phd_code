import unittest
from mock import MagicMock
from process_config import couchdb_config_parser
from process_config.add_history import add_history_item
from process_config import notification_registration_client
from process_config import edit_wifi
from undo import perform_undo
from undo.doc_types import notifications
import time


class TestPerformUndo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = couchdb_config_parser.get_db()

    @classmethod
    def tearDownClass(cls):
        vr = cls.db.view('homework-remote/events')
        vra = vr.all()
        for row in vra:
            current = cls.db.get(row['id'])
            current['_deleted'] = True
            cls.db.save_doc(current, force_update=True)
        cls.db = None

    def test_process_undo_notification_new_doc(self):
        nd = {
            "collection": "notifications",
            "status": "done",
            "name": "Rob",
            "service": "twitter",
            "user": "rjspencer1989"
        }

        res = self.db.save_doc(nd)
        notification_registration_client.registration(nd)
        nd = self.db.get(nd['_id'])
        title = "new notification"
        desc = "added rjspencer1989 as twitter username for Rob"
        doc_arr = [{'doc_id': res['id'], 'doc_rev': res['rev'], 'doc_collection': 'notifications', 'action': 'add'}]
        event_res = add_history_item(title, desc, doc_arr, undoable=True)
        event = self.db.get(event_res['id'])
        result = perform_undo.perform_undo(event)
        updated = self.db.get(nd['_id'], rev=result)
        self.assertTrue('hidden' in updated)
        event['_deleted'] = True
        self.db.save_doc(event, force_update=True)

    def test_process_undo_notification_delete_doc(self):
        nd = {
            "collection": "notifications",
            "status": "done",
            "name": "Rob",
            "service": "twitter",
            "user": "rjspencer1989"
        }

        self.db.save_doc(nd)
        notification_registration_client.registration(nd)
        nd = self.db.get(nd['_id'])
        nd['hidden'] = True
        res = self.db.save_doc(nd)
        title = "Deleted Notification"
        desc = "Removed rjspencer1989 as twitter username for Rob"
        doc_arr = [{'doc_id': res['id'], 'doc_rev': res['rev'], 'doc_collection': 'notifications', 'action': 'delete'}]
        event_res = add_history_item(title, desc, doc_arr, undoable=True)
        event = self.db.get(event_res['id'])
        result = perform_undo.perform_undo(event)
        updated = self.db.get(nd['_id'], rev=result)
        self.assertTrue('hidden' not in updated)
        self.assertTrue('suid' in updated)
        event['_deleted'] = True
        self.db.save_doc(event, force_update=True)

    def test_process_undo_notification_edit_doc(self):
        nd = {
            "collection": "notifications",
            "status": "done",
            "name": "Rob",
            "service": "twitter",
            "user": "rjspencer1989"
        }
        res = self.db.save_doc(nd)
        notification_registration_client.registration(nd)
        nd['user'] = 'robjspencer'
        res2 = self.db.save_doc(nd, force_update=True)
        title = "Edit Notification"
        desc = "Edited twitter username for Rob now identified by robjspencer"
        doc_arr = [{'doc_id': res2['id'], 'doc_rev': res2['rev'], 'doc_collection': 'notifications', 'action': 'edit'}]
        event_res = add_history_item(title, desc, doc_arr, True)
        event = self.db.get(event_res['id'])
        result = perform_undo.perform_undo(event)
        updated = self.db.get(nd['_id'], rev=result)
        self.assertEqual(updated['user'], 'rjspencer1989')
        nd['hidden'] = True
        self.db.save_doc(nd, force_update=True)
        event['_deleted'] = True
        self.db.save_doc(event, force_update=True)

    def test_process_undo_device_doc(self):
        doc = {
            "_id": "11:aa:33:bb:cc:ff",
            "action": "",
            "collection": "devices",
            "device_name": "",
            "host_name": "test-device",
            "ip_address": "10.2.0.61",
            "lease_action": "add",
            "mac_address": "11:aa:33:bb:cc:ff",
            "name": "",
            "state": "pending",
            "device_type": "",
            "notification_service": "",
            "timestamp": time.time(),
            "connection_event": "connect",
            "changed_by": "system"
        }
        self.db.save_doc(doc)  # initial from DHCP
        doc['action'] = 'deny'
        doc['device_name'] = 'test-device'
        doc['name'] = 'Rob'
        doc['device_type'] = 'laptop'
        doc['notification_service'] = 'phone'
        doc['changed_by'] = 'user'
        self.db.save_doc(doc)  # initial user decision
        doc['action'] = ''
        doc['state'] = 'deny'
        doc['changed_by'] = 'system'
        self.db.save_doc(doc)  # POX applying change
        doc['action'] = 'permit'
        doc['changed_by'] = 'user'
        res = self.db.save_doc(doc)  # user changes their mind
        title = "Permit Device"
        desc = "Permitted Test Device"
        doc_arr = [{'doc_id': res['id'], 'doc_rev': res['rev'], 'doc_collection': 'devices', 'action': 'edit'}]
        event_res = add_history_item(title, desc, doc_arr, True)
        event = self.db.get(event_res['id'])
        result = perform_undo.perform_undo(event)
        updated = self.db.open_doc(doc['_id'], rev=result)
        self.assertEqual('deny', updated['action'])
        event['_deleted'] = True
        doc['_deleted'] = True
        self.db.save_doc(doc, force_update=True)
        self.db.save_doc(event, force_update=True)

    def test_process_undo_wifi_edit_doc(self):
        nd = {
            "collection": "wifi",
            "status": "pending",
            "ssid": "test",
            "channel": 1,
            "mode": "g",
            "encryption_type": "wpa",
            "password_type": "txt",
            "password": "whatever12345",
        }
        cons = edit_wifi
        keys = ['interface',
                'bridge',
                'driver',
                'ssid',
                'hw_mode',
                'channel',
                'ieee80211n',
                'macaddr_acl',
                'auth_algs',
                'ignore_broadcast_ssid',
                'eapol_key_index_workaround',
                'eap_server',
                'own_ip_addr',
                'wpa',
                'wpa_passphrase',
                'wpa_key_mgmt',
                'wpa_pairwise',
                'rsn_pairwise']
        values = ['wlan0',
                  'br0',
                  'nl80211',
                  'test_old',
                  'g',
                  '1',
                  '1',
                  '0',
                  '1',
                  '0',
                  '0',
                  '0',
                  '127.0.0.1',
                  '3',
                  'whatever',
                  'WPA-PSK',
                  'TKIP',
                  'CCMP']
        cons.get_config = MagicMock(return_value=(keys, values))
        res = self.db.save_doc(nd)
        nd['status'] = 'done'
        self.db.save_doc(nd, force_update=True)
        nd['ssid'] = 'robjspencer'
        nd['status'] = 'pending'
        res3 = self.db.save_doc(nd, force_update=True)
        title = "edit wifi"
        desc = "Edited wifi config"
        doc_arr = [{'doc_id': nd['_id'], 'doc_rev': res3['rev'], 'doc_collection': 'wifi', 'action': 'edit'}]
        event_res = add_history_item(title, desc, doc_arr, True)
        event = self.db.get(event_res['id'])
        result = perform_undo.perform_undo(event)
        updated = self.db.get(nd['_id'], rev=result)
        self.assertEqual(updated['ssid'], 'test')
        nd['_deleted'] = True
        self.db.save_doc(nd, force_update=True)
        event['_deleted'] = True
        self.db.save_doc(event, force_update=True)
