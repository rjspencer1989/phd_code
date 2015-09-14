import unittest
from process_config import couchdb_config_parser, perform_rollback, add_history, edit_wifi
import datetime
from mock import MagicMock
from dateutil.tz import tzutc
import pprint


class TestProcessRollback(unittest.TestCase):
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

    @classmethod
    def tearDownClass(cls):
        current_events = cls.db.view('homework-remote/events')
        if current_events.count() > 0:
            current_events_all = current_events.all()
            for row in current_events_all:
                current_doc = cls.db.get(row['id'])
                current_doc['_deleted'] = True
                cls.db.save_doc(current_doc, force_update=True)
        cls.db = None

    def setUp(self):
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
            "channel": 1,
            "with_bss": False
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
        self.expected_line_list = [
            'interface=wlan0\n',
            'bridge=br0\n',
            'driver=nl80211\n',
            'ssid=test_old\n',
            'hw_mode=g\n',
            'channel=1\n',
            'ieee80211n=1\n',
            'macaddr_acl=0\n',
            'auth_algs=1\n',
            'ignore_broadcast_ssid=0\n',
            'eapol_key_index_workaround=0\n',
            'eap_server=0\n',
            'own_ip_addr=127.0.0.1\n',
            'wpa=3\n',
            'wpa_passphrase=whatever\n',
            'wpa_key_mgmt=WPA-PSK\n',
            'wpa_pairwise=TKIP\n',
            'rsn_pairwise=CCMP\n',
            'bss=wlan0_1\n',
            'ssid=test\n',
            'wpa=3\n',
            'wpa_passphrase=whatever\n',
            'wpa_key_mgmt=WPA-PSK\n',
            'wpa_pairwise=TKIP\n',
            'rsn_pairwise=CCMP'
        ]
        res1 = self.db.save_doc(self.wifi_doc)
        self.test_doc_ids.append(res1['id'])
        dt = datetime.datetime(2015, 1, 5, hour=10, minute=5)
        doc_arr = [{'doc_id': res1['id'], 'doc_rev': res1['rev'], 'doc_collection': 'wifi', 'action': 'edit'}]
        self.hist1 = add_history.add_history_item(self.title, self.description, doc_arr, True, ts=dt.isoformat())
        self.test_doc_ids.append(self.hist1['id'])
        self.wifi_doc['ssid'] = 'testing2'
        res2 = self.db.save_doc(self.wifi_doc)
        dt = datetime.datetime(2015, 2, 5, hour=10, minute=5)
        doc_arr = [{'doc_id': res2['id'], 'doc_rev': res2['rev'], 'doc_collection': 'wifi', 'action': 'edit'}]
        self.hist2 = add_history.add_history_item(self.title, self.description, doc_arr, True, ts=dt.isoformat())
        self.test_doc_ids.append(self.hist2['id'])
        self.wifi_doc['ssid'] = 'testing3'
        res3 = self.db.save_doc(self.wifi_doc)
        dt = datetime.datetime(2015, 2, 23, hour=15, minute=0)
        doc_arr = [{'doc_id': res3['id'], 'doc_rev': res3['rev'], 'doc_collection': 'wifi', 'action': 'edit'}]
        self.hist3 = add_history.add_history_item(self.title, self.description, doc_arr, True, ts=dt.isoformat())
        self.test_doc_ids.append(self.hist3['id'])
        res4 = self.db.save_doc(self.notification_doc)
        self.test_doc_ids.append(res4['id'])
        self.notification_doc = self.db.get(res4['id'])
        pprint.pprint(self.notification_doc)
        dt = datetime.datetime(2015, 2, 12, hour=14, minute=34)
        doc_arr = [{'doc_id': res4['id'], 'doc_rev': res4['rev'], 'doc_collection': 'notifications', 'action': 'add'}]
        self.notification_doc = self.db.get(res4['id'])
        self.hist4 = add_history.add_history_item(self.title, self.description, doc_arr, True, ts=dt.isoformat())
        self.test_doc_ids.append(self.hist4['id'])
        self.rb = perform_rollback.Rollback(self.db, self.revert_doc)

    def tearDown(self):
        self.expected_line_list = []
        for doc in self.test_doc_ids:
            opened = self.db.get(doc)
            opened['_deleted'] = True
            self.db.save_doc(opened, force_update=True)

    def test_process_rollback_get_events(self):
        result = self.rb.get_events_after_timestamp(self.revert_doc['timestamp'])
        result_list = list(result)
        self.assertEqual(3, len(result_list))

    def test_process_rollback_get_docs_to_revert(self):
        result = self.rb.get_docs_to_revert(self.revert_doc['timestamp'])
        self.assertEqual(2, len(result))
        k = result.keys()
        self.assertNotEqual(k[0], k[1])

    def test_rollback(self):
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
        result = self.rb.revert(self.revert_doc['timestamp'])
        self.assertTrue(result)
