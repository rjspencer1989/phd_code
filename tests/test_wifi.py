import unittest
from mock import MagicMock
from process_config import edit_wifi


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
            'rsn_pairwise=CCMP\n'
        ]

    def tearDown(self):
        self.current_doc = {}
        self.expected_line_list = []

    def test_wifi(self):
        cons = edit_wifi.consumer
        cons.get_config = MagicMock(return_value={'interface': 'wlan0'})
        retVal = cons.generate_config(self.current_doc)
        self.assertListEqual(self.expected_line_list, retVal)
