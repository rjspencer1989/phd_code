import unittest
from mock import MagicMock
from process_config import edit_wifi
import pprint


class TestWifi(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.current_doc = {
            "ssid": "test",
            "encryption_type": "wpa",
            "mode": "n",
            "channel": 1,
            "password": "whatever"
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

    def tearDown(self):
        self.current_doc = {}
        self.expected_line_list = []

    def test_wifi(self):
        cons = edit_wifi
        keys = ['interface', 'bridge', 'driver', 'ssid', 'hw_mode', 'channel', 'ieee80211n', 'macaddr_acl', 'auth_algs', 'ignore_broadcast_ssid', 'eapol_key_index_workaround', 'eap_server', 'own_ip_addr', 'wpa', 'wpa_passphrase', 'wpa_key_mgmt', 'wpa_pairwise', 'rsn_pairwise']
        values = ['wlan0', 'br0', 'nl80211', 'test_old', 'g', '1', '1', '0', '1', '0', '0', '0', '127.0.0.1', '3', 'whatever', 'WPA-PSK', 'TKIP', 'CCMP']
        cons.get_config = MagicMock(return_value=(keys, values))
        retVal = cons.generate_config(self.current_doc)
        self.assertListEqual(self.expected_line_list, retVal)
