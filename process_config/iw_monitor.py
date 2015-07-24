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

disconnected = [x for x in keys if x not in connected_macs]
pprint.pprint(disconnected)
