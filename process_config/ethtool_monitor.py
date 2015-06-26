#!/usr/bin/env python

import netifaces
from couchdbkit import *
from subprocess import *
import couchdb_config_parser
import time
from add_history import add_history_item

db = couchdb_config_parser.get_db()
interface_list = netifaces.interfaces()
ethernet_list = filter(lambda x: 'eth' in x, interface_list)
if 'eth0 in ethernet_list':
    ethernet_list.remove('eth0')
while True:
    for iface in ethernet_list:
        result = Popen(['ethtool', iface], stdout=PIPE).communicate()[0]
        lines = result.splitlines()
        vr = db.view('homework-remote/ports', key=iface)
        rows = vr.all()
        print rows
        if len(list(rows)) > 0:
            row = rows[0]
            mac_address = row['value']
            device_doc = db.get(mac_address)
            name = device_doc['device_name']
            if device_doc['device_name'] == '':
                name = device_doc['mac_address']

            if "\tLink detected: yes" in lines:
                if device_doc['connection_event'] == 'disconnect':
                    device_doc['connection_event'] = 'connect'
                    device_doc['changed_by'] = 'connected_devices'
                    res = db.save_doc(device_doc)
                    title = 'Device connected'
                    desc = '%s connected' % (name)
                    add_history_item(title, desc, res['id'], res['rev'], False)
            else:
                if device_doc['connection_event'] == 'connect':
                    device_doc['connection_event'] = 'disconnect'
                    device_doc['changed_by'] = 'connected_devices'
                    res = db.save_doc(device_doc)
                    title = 'Device disconnected'
                    desc = '%s disconnected' % (name)
                    add_history_item(title, desc, res['id'], res['rev'], False)
    time.sleep(1)
