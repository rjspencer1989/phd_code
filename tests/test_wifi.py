import unittest
from process_config import edit_wifi


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
            'channel=1\n',
            'beacon_int=100\n',
            'dtim_period=2\n',
            'max_num_sta=255\n',
            'rts_threshold=2347\n',
            'fragm_threshold=2346\n',
            'macaddr_acl=0\n',
            'auth_algs=3\n',
            'ignore_broadcast_ssid=0\n',
            'wme_enabled=0\n',
            'wme_ac_bk_cwmin=4\n',
            'wme_ac_bk_cwmax=10\n',
            'wme_ac_bk_aifs=7\n',
            'wme_ac_bk_txop_limit=0\n',
            'wme_ac_bk_acm=0\n',
            'wme_ac_be_aifs=3\n',
            'wme_ac_be_cwmin=4\n',
            'wme_ac_be_cwmax=10\n',
            'wme_ac_be_txop_limit=0\n',
            'wme_ac_be_acm=0\n',
            'wme_ac_vi_aifs=2\n',
            'wme_ac_vi_cwmin=3\n',
            'wme_ac_vi_cwmax=4\n',
            'wme_ac_vi_txop_limit=94\n',
            'wme_ac_vi_acm=0\n',
            'wme_ac_vo_aifs=2\n',
            'wme_ac_vo_cwmin=2\n',
            'wme_ac_vo_cwmax=3\n',
            'wme_ac_vo_txop_limit=47\n',
            'wme_ac_vo_acm=0\n',
            'eapol_key_index_workaround=0\n',
            'eap_server=0\n',
            'own_ip_addr=127.0.0.1\n',
            'wep_default_key=0\n'
        ]

    def tearDown(self):
        self.current_doc = {}
        self.expected_line_list = []

    def test_wifi_text_password(self):
        self.current_doc['password_type'] = 'txt'
        self.current_doc['password'] = 'whatever12345'
        self.expected_line_list.append('wep_key0=\"whatever12345\"\n')
        retVal = edit_wifi.consumer.generate_config(self.current_doc)
        self.assertListEqual(self.expected_line_list, retVal)

    def test_wifi_hex_password(self):
        self.current_doc['password_type'] = 'hex'
        self.current_doc['password'] = 'deadbeefdeadbeefdeadbeef01'
        self.expected_line_list.append('wep_key0=deadbeefdeadbeefdeadbeef01\n')
        retVal = edit_wifi.consumer.generate_config(self.current_doc)
        self.assertListEqual(self.expected_line_list, retVal)
