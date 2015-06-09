#!/usr/bin/env python
import time
import os
import couchdb_config_parser
from couchdbkit import *

filename = '/var/log/syslog'
file = open(filename, 'r')
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

db = couchdb_config_parser.get_db()

while 1:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        hostapd_index = line.find('hostapd')

        if hostapd_index > -1:
            if line.find('associated') > -1:
                chunks = line.split()
                mac_address = chunks[7]
                action = chunks[10]
                device_doc = db.get(mac_address)
                if device_doc['connection_event'] == 'connect' and action == 'disassociated':
                    device_doc['connection_event'] = 'disconnect'
                    device_doc['changed_by'] = 'connected_devices'
                    db.save_doc(device_doc)
                    continue
                elif device_doc['connection_event'] == 'disconnect' and action == 'associated':
                    device_doc['connection_event'] = 'connect'
                    device_doc['changed_by'] = 'connected_devices'
                    db.save_doc(device_doc)
                    continue
