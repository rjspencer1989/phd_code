import unittest
from process_config import remove_vlan
from mock import MagicMock


class TestRemoveVlan(unittest.TestCase):
    def test_remove_vlan(self):
        self.maxDiff = None
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
                  'test',
                  'whatever',
                  'WPA-PSK',
                  'TKIP',
                  'CCMP']
        mod = remove_vlan
        mod.get_config = MagicMock(return_value=(keys, values))
        self.assertEqual((['interface'], ['wlan0']), mod.remove_vlan())
