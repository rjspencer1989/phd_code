import unittest
from process_config import edit_wifi


class TestWifi(unittest.TestCase):
    def setUp(self):
        self.current_doc = {
            "ssid": "test",
            "encryption_type": "wpa",
            "mode": "n",
            "channel": 1,
            "password": "whatever"
        }

        self.expected_line_list = [
            'interface=wlan0\n',
            'driver=nl80211\n',
            'logger_syslog=-1\n',
            'logger_syslog_level=2\n',
            'logger_stdout=-1\n',
            'logger_stdout_level=2\n',
            'debug=0\n',
            'dump_file=/tmp/hostapd.dump\n',
            'ctrl_interface=/var/run/hostapd\n',
            'ctrl_interface_group=0\n',
            'ssid=test\n',
            'hw_mode=g\n',
            'ieee80211n=1\n',
            'channel=1\n',
            'beacon_int=100\n',
            'dtim_period=2\n',
            'max_num_sta=255\n',
            'rts_threshold=2347\n',
            'fragm_threshold=2346\n',
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
            'rsn_pairwise=CCMP\n'
        ]

    def tearDown(self):
        self.current_doc = {}
        self.expected_line_list = []

    def test_wifi(self):
        retVal = edit_wifi.consumer.generate_config(self.current_doc)
        self.assertListEqual(self.expected_line_list, retVal)
