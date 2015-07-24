#!/usr/bin/env python

import subprocess
from couchdbkit import *
from process_config import couchdb_config_parser
import pprint
from apscheduler.schedulers.background import BackgroundScheduler
import time

db = couchdb_config_parser.get_db()


def update_device_list():
    connected_macs = []
    keys = []
    result = subprocess.check_output(['iw', 'dev', 'wlan0', 'station', 'dump'])
    lines = result.split('\n')
    for line in lines:
        if line.startswith('Station'):
            fields = line.split(' ')
            mac_addr = fields[1]
            connected_macs.append(mac_addr)

    vr = db.view('homework-remote/wlan0')
    for item in vr.all():
        keys.append(item['key'])

    disconnected = [x for x in keys if x not in connected_macs]
    for device in connected_macs:
        if not db.doc_exist(device):
            continue
        doc = db.get(device)
        print "[%s - %s]\n" % (doc['_id'], doc['connection_event'])
        if doc['connection_event'] != 'connect':
            doc['connection_event'] = 'connect'
            doc['changed_by'] = 'connected_devices'
            db.save_doc(doc, force_update=True)

    print "disconnected:\n"
    for device in disconnected:
        if not db.doc_exist(device):
            continue
        doc = db.get(device)
        print "[%s - %s]\n" % (doc['_id'], doc['connection_event'])
        if doc['connection_event'] != 'disconnect':
            doc['connection_event'] = 'disconnect'
            doc['changed_by'] = 'connected_devices'
            db.save_doc(doc, force_update=True)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_device_list, 'interval', seconds=5)
    scheduler.start()
    print 'press ctrl+c to exit'

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
