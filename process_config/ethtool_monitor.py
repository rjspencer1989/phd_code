#!/usr/bin/env python

import netifaces
from couchdbkit import *
from subprocess import *
import couchdb_config_parser
import time
from change_notification import sendNotification

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
            if not db.doc_exist(mac_address):
                continue
            device_doc = db.get(mac_address)
            name = device_doc['device_name']
            if device_doc['device_name'] == '':
                name = '%s (%s)' % (device_doc['mac_address'], device_doc['host_name'])

            if "\tLink detected: yes" in lines:
                if device_doc['connection_event'] == 'disconnect':
                    device_doc['connection_event'] = 'connect'
                    device_doc['changed_by'] = 'connected_devices'
                    if device_doc['state'] == 'pending':
                        main_doc = db.get('main_user')
                        user = main_doc['name']
                        service = main_doc['service']
                        msg = "%s is requesting access to your network" % (name)
                        sendNotification(user, service, msg)
                    res = db.save_doc(device_doc)
            else:
                if device_doc['connection_event'] == 'connect':
                    device_doc['connection_event'] = 'disconnect'
                    device_doc['changed_by'] = 'connected_devices'
                    res = db.save_doc(device_doc)
    time.sleep(1)
