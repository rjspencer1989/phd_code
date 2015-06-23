import unittest
import remove_vlan
from mock import MagicMock

class TestRemoveVlan(unittest.TestCase):
    def test_remove_vlan(self):
        keys = ['interface']
        values = ['wlan0']
        mod = remove_vlan
        mod.get_config = MagicMock(return_value=(keys, values))
        self.assertEqual((['interface'], ['wlan0']), mod.get_config())
