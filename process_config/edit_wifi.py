#!/usr/bin/env python

from couchdbkit import *
from Queue import Queue
import threading
import datetime
import couchdb_config_parser
import subprocess
import change_notification
import os
import add_history
import remove_vlan
from apscheduler.schedulers.background import BackgroundScheduler

db = couchdb_config_parser.get_db()


def get_connected_devices():
    vr = db.view('homework-remote/connected_via_wifi')
    return vr.all()


def notify(devices, ssid):
    if devices is not None and len(devices) > 0:
        for row in devices:
            if (len(row['value']['notification_service']) > 0 and
                    len(row['value']['name']) > 0):
                service = row['value']['notification_service']
                to = row['value']['name']
                timestr = datetime.datetime.now().strftime("%H:%M:%S")
                msg = "Hi %s. A new network was created at %s. You need to connect %s to this new network. The new network name is %s. The current network will be turned off in 24 hours, and %s won't be able to connect" % (to, timestr, row['value']['device_name'], ssid, row['value']['device_name'])
                change_notification.sendNotification(to, service, msg)
    return True


def get_config():
    with open('/etc/hostapd/hostapd.conf', 'r') as fh:
        keys = []
        values = []
        lines = fh.readlines()
        for line in lines:
            arr = line.split('=')
            keys.append(arr[0])
            values.append(arr[1].strip())
        return (keys, values)


def write_config_file(lines):
    with open('/etc/hostapd/hostapd.conf', 'w') as fh:
        fh.writelines(lines)


def reload_hostapd():
    cmd = ['/etc/init.d/hostapd', 'restart']
    res = subprocess.call(cmd)


def add_vlan_to_bridge():
    cmd = ['/usr/local/bin/ovs-vsctl', '--if-exists', 'del-port', 'br0', 'wlan0_1']
    subprocess.call(cmd)
    cmd = ['/usr/local/bin/ovs-vsctl', 'add-port', 'br0', 'wlan0_1']
    subprocess.call(cmd)


def generate_config(current_doc, with_bss=True):
    line_list = get_config()
    keys = line_list[0]
    values = line_list[1]
    lines = []
    if len(keys) > 0:
        channel_index = keys.index('channel')
        values[channel_index] = current_doc['channel']
        if current_doc['mode'] == 'n' and 'ieee80211n' not in keys:
            keys.append('ieee80211n')
            values.append('1\n')
        elif current_doc['mode'] == 'g' and 'ieee80211n' in keys:
            n_index = keys.index('ieee80211n')
            keys.pop(n_index)
            values.pop(n_index)

        if 'bss' in keys:
            bss_index = keys.index('bss')
            keys = keys[0:bss_index]
            values = values[0:bss_index]
        if with_bss is True:
            for key, value in zip(keys, values):
                line = '{0}={1}\n'.format(key, value)
                lines.append(line)
            lines.append('bss=wlan0_1\n')
            lines.append('ssid=%s\n' % (current_doc['ssid']))
            lines.append('wpa=3\n')
            lines.append('wpa_passphrase=%s\n' % (current_doc['password']))
            lines.append('wpa_key_mgmt=WPA-PSK\n')
            lines.append('wpa_pairwise=TKIP\n')
            lines.append('rsn_pairwise=CCMP')
        else:
            ssid_index = keys.index('ssid')
            values[ssid_index] = current_doc['ssid']
            passphrase_index = keys.index('wpa_passphrase')
            values[passphrase_index] = current_doc['password']
            for key, value in zip(keys, values):
                line = '{0}={1}\n'.format(key, value)
                lines.append(line)
    return lines


def process_wifi(doc, from_undo=False):
    bss = True
    if 'with_bss' in doc and doc['with_bss'] == True:
        line_list = generate_config(doc)
    else:
        line_list = generate_config(doc, False)
        bss = False
    devices = get_connected_devices()
    doc['with_bss'] = True
    doc['status'] = 'done'
    ts = None
    if 'event_timestamp' in doc:
        ts = doc['event_timestamp']
        del doc['event_timestamp']
    title = "New WiFi Configuration"
    desc = "WiFi configuration has been updated. "
    desc += "You will need to reconnect your devices"
    undoable = True
    if from_undo is True:
        title = "Undo change to WiFi Configuration"
    if doc['_rev'].startswith('1-'):
        title = 'Initial WiFi Configuration'
        desc = 'WiFi initialised with default values.'
        undoable = False
    doc_arr = [{'doc_id': doc['_id'], 'doc_rev': doc['_rev'], 'doc_collection': 'wifi', 'action': 'edit'}]
    add_history.add_history_item(title, desc, doc_arr, undoable=undoable, ts=ts)
    db.save_doc(doc, force_update=True)
    if 'ENV_TESTS' not in os.environ:
        write_config_file(line_list)
        if bss is False:
            if notify(devices, doc['ssid']):
                reload_hostapd()
                add_vlan_to_bridge()
                if bss is True:
                    scheduler = BackgroundScheduler()
                    cur_time = datetime.datetime.now()
                    dt = cur_time + datetime.timedelta(days=1)
                    scheduler.add_job(remove_vlan.remove_vlan, 'date', run_date=dt)
                    scheduler.start()
