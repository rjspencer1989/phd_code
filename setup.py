#!/usr/bin/env python

from couchdbkit import *

from process_config import couchdb_config_parser

import random
import string
import subprocess

db = couchdb_config_parser.get_db()
db.flush()

ssid = "homework-%d" % (int(random.getrandbits(25)))
password = ''.join(random.sample(string.ascii_lowercase+string.digits, 10))
print password
channel = random.choice(range(1,12))

wifi = {
    'collection': 'wifi',
    'status': 'done',
    'ssid': ssid,
    'encryption_type': 'wpa',
    'password': password,
    'mode': 'n',
    'channel': channel
}

res = db.save_doc(wifi, force_update=True)

lines = ['auth_algs=1\n',
         'bridge=br0\n',
         'channel=%d\n' % (channel),
         'ctrl_interface=/var/run/hostapd\n',
         'ctrl_interface_group=0\n',
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
         'ssid=%s\n' % (ssid),
         'wpa=3\n',
         'wpa_key_mgmt=WPA-PSK\n',
         'wpa_pairwise=TKIP\n',
         'wpa_passphrase=%s\n' % (password)]
 
with open('/etc/hostapd/hostapd.conf', 'w') as fh:
    fh.writelines(lines)
subprocess.call(['/sbin/reboot'])
