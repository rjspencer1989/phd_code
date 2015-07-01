#!/usr/bin/env python
import time
import os
import couchdb_config_parser
from couchdbkit import *
from add_history import add_history_item
from change_notification import sendNotification

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
                name = device_doc['device_name']
                if device_doc['device_name'] == '':
                    name = device_doc['mac_address']
                if (device_doc['connection_event'] == 'connect' and
                        action == 'disassociated'):
                    device_doc['connection_event'] = 'disconnect'
                    device_doc['changed_by'] = 'connected_devices'
                    res = db.save_doc(device_doc)
                    title = 'Device disconnected'
                    desc = '%s disconnected' % (name)
                    add_history_item(title, desc, res['id'], res['rev'], False)
                    continue
                elif (device_doc['connection_event'] == 'disconnect' and
                        action == 'associated'):
                    device_doc['connection_event'] = 'connect'
                    device_doc['changed_by'] = 'connected_devices'
                    if device_doc['state'] == 'pending':
                        main_doc = db.get('main_user')
                        user = main_doc['name']
                        service = main_doc['service']
                        msg = "%s is requesting access to your network" % (name)
                        sendNotification(user, service, msg)
                    res = db.save_doc(device_doc)
                    title = 'Device connected'
                    desc = '%s connected' % (name)
                    add_history_item(title, desc, res['id'], res['rev'], False)
                    continue
