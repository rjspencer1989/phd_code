#!/usr/bin/env python

import subprocess
from couchdbkit import *
from process_config import couchdb_config_parser
import pprint

db = couchdb_config_parser.get_db()
connected_macs = []
keys = []
result = subprocess.check_output(['iw', 'dev', 'wlan0', 'station', 'dump'])
lines = result.split('\n')
for line in lines:
    if line.startswith('Station'):
        fields = line.split(' ')
        mac_addr = fields[1]
        connected_macs.append(mac_addr)

vr = db.view('homework-remote/dhcp')
for item in vr.all():
    keys.append(item['key'])

disconnected = list({x for x in key_set if x not in connected})
pprint.pprint(disconnected)
