#!/usr/bin/env python

import netifaces
from couchdbkit import *
from subprocess import *
import couchdb_config_parser
import time

db = couchdb_config_parser.get_db()
interface_list = netifaces.interfaces()
ethernet_list = filter(lambda x: 'eth' in x, interface_list)
if 'eth0 in ethernet_list':
    ethernet_list.remove('eth0')
while True:
    for iface in ethernet_list:
        vr = db.view('homework-remote/ports', key=iface)
        rows = vr.all()
        print rows
        if len(list(rows)) > 0:
            row = rows[0]
            mac_address = row['value']
            device_doc = db.get(mac_address)
        result = Popen(['ethtool', iface], stdout=PIPE).communicate()[0]
        lines = result.splitlines()
        print "\tLink detected: yes" in lines
        if "\tLink detected: yes" in lines:
            if device_doc['connection_event'] == 'disconnect':
                device_doc['connection_event'] = 'connect'
                device_doc['changed_by'] = 'connected_devices'
                db.save_doc(device_doc)
        else:
            if device_doc['connection_event'] == 'connect':
                device_doc['connection_event'] = 'disconnect'
                device_doc['changed_by'] = 'connected_devices'
                db.save_doc(device_doc)
    time.sleep(1)
