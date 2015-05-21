import unittest
from process_config import wifi


class TestWifi(unittest.TestCase):
    def setUp(self):
        self.current_doc = {
            "ssid": "test",
            "encryption_type": "wep",
            "mode": "g",
            "channel": 1
        }

        self.expected_line_list = [
            'interface=wlan0\n',
            'driver=nl80211\n',
            'ctrl_interface=/var/run/hostapd\n',
            'ctrl_interface_group=0\n',
            'hw_mode=g\n',
            'auth_algs=3\n',
            'channel=1\n',
            'eapol_key_index_workaround=0\n',
            'eap_server=0\n',
            'own_ip_addr=127.0.0.1\n',
            'wep_default_key=0\n',
            'ignore_broadcast_ssid=0\n',
            'ssid=test\n'
        ]

    def tearDown(self):
        self.current_doc = {}
        self.expected_line_list = []

    def test_wifi_text_password(self):
        self.current_doc['password_type'] = 'txt'
        self.current_doc['password'] = 'whatever12345'
        self.expected_line_list.append('wep_key0=\"whatever12345\"\n')
        retVal = wifi.consumer.generate_config(self.current_doc)
        self.assertListEqual(self.expected_line_list, retVal)

    def test_wifi_hex_password(self):
        self.current_doc['password_type'] = 'hex'
        self.current_doc['password'] = 'deadbeefdeadbeefdeadbeef01'
        self.expected_line_list.append('wep_key0=deadbeefdeadbeefdeadbeef01\n')
        retVal = wifi.consumer.generate_config(self.current_doc)
        self.assertListEqual(self.expected_line_list, retVal)
