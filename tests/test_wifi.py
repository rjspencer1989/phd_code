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
            'auth_algs=1\n',
            'bridge=br0\n',
            'channel=1\n',
            'driver=nl80211\n',
            'eap_server=0\n',
            'eapol_key_index_workaround=0\n',
            'hw_mode=g\n',
            'ieee80211n=1\n',
            'ignore_broadcast_ssid=0\n',
            'interface=wlan0\n',
            'macaddr_acl=0\n',
            'own_ip_addr=127.0.0.1\n',
            'rsn_pairwise=CCMP\n',
            'ssid=test_old\n',
            'wpa=3\n',
            'wpa_key_mgmt=WPA-PSK\n',
            'wpa_pairwise=TKIP\n',
            'wpa_passphrase=whatever\n'
            # 'bss=wlan0_1\n',
            # 'ssid=test\n',
            # 'wpa=3\n',
            # 'wpa_passphrase=whatever\n',
            # 'wpa_key_mgmt=WPA-PSK\n',
            # 'wpa_pairwise=TKIP\n',
            # 'rsn_pairwise=CCMP\n'
        ]

    def tearDown(self):
        self.current_doc = {}
        self.expected_line_list = []

    def test_wifi(self):
        cons = edit_wifi.consumer
        cons.get_config = MagicMock(return_value={'interface': 'wlan0',
                                                  'bridge': 'br0',
                                                  'driver': 'nl80211',
                                                  'ssid': 'test_old',
                                                  'hw_mode': 'g',
                                                  'channel': '1',
                                                  'ieee80211n': '1',
                                                  'macaddr_acl': '0',
                                                  'auth_algs': '1',
                                                  'ignore_broadcast_ssid': '0',
                                                  'eapol_key_index_workaround': '0',
                                                  'eap_server': '0',
                                                  'own_ip_addr': '127.0.0.1',
                                                  'wpa': '3',
                                                  'wpa_passphrase': 'whatever',
                                                  'wpa_key_mgmt': 'WPA-PSK',
                                                  'wpa_pairwise': 'TKIP',
                                                  'rsn_pairwise': 'CCMP'})
        retVal = cons.generate_config(self.current_doc)
        pprint.pprint(retVal)
        self.assertListEqual(self.expected_line_list, retVal)
