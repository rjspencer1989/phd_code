import unittest
from process_config import remove_vlan
from mock import MagicMock


class TestRemoveVlan(unittest.TestCase):
    def test_remove_vlan(self):
        self.maxDiff = None
        expected = ['interface=wlan0\n',
                    'bridge=br0\n',
                    'driver=nl80211\n',
                    'ssid=test\n',
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
                    'wpa_passphrase=whatever_next\n',
                    'wpa_key_mgmt=WPA-PSK\n',
                    'wpa_pairwise=TKIP\n',
                    'rsn_pairwise=CCMP\n']
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
                'rsn_pairwise',
                'bss',
                'ssid',
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
                  'CCMP',
                  'wlan0_1',
                  'test',
                  '3',
                  'whatever_next',
                  'WPA-PSK',
                  'TKIP',
                  'CCMP']
        mod = remove_vlan
        mod.get_config = MagicMock(return_value=(keys, values))
        self.assertListEqual(expected, mod.generate_config())
