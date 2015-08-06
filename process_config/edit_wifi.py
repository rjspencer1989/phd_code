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
import pprint
import remove_vlan
from apscheduler.schedulers.background import BackgroundScheduler

db = couchdb_config_parser.get_db()


def get_connected_devices():
    vr = db.view('homework-remote/connected_devices')
    return vr.all()


def notify(devices):
    if devices is not None and len(devices) > 0:
        for row in devices:
            if (len(row['value']['notification_service']) > 0 and
                    len(row['value']['name']) > 0):
                service = row['value']['notification_service']
                to = row['value']['name']
                timestr = datetime.datetime.now().strftime("%H:%M:%S")
                msg = "network settings updated at %s" % (timestr)
                change_notification.sendNotification(to, service, msg)
    return True


def get_config():
    with open('/etc/hostapd/hostapd.conf', 'r') as fh:
        keys = []
        values = []
        lines = fh.readlines()
        for line in lines:
            print line
            arr = line.split('=')
            keys.append(arr[0])
            values.append(arr[1].strip())
        return (keys, values)


def write_config_file(lines):
    with open('/etc/hostapd/hostapd.conf', 'w') as fh:
        fh.writelines(lines)


def reload_hostapd():
    cmd = ['/etc/init.d/hostapd', 'restart']
    res = subprocess.Popen(cmd)


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
    print keys
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


def process_wifi(doc):
    bss = True
    if 'with_bss' in doc and doc['with_bss'] == True:
        line_list = generate_config(doc)
    else:
        line_list = generate_config(doc, False)
        bss = False
    write_config_file(line_list)
    devices = get_connected_devices()
    doc['with_bss'] = True
    doc['status'] = 'done'
    ts = None
    if 'event_timestamp' in doc:
        ts = doc['event_timestamp']
        del doc['event_timestamp']
    db.save_doc(doc)
    title = "New WiFi Configuration"
    desc = "WiFi configuration has been updated. "
    desc += "You will need to reconnect your devices"
    undoable = False if doc['_rev'].startswith('1-') else True
    add_history.add_history_item(title, desc, doc['_id'], doc['_rev'], undoable, ts=ts)
    if notify(devices):
        reload_hostapd()
        add_vlan_to_bridge()
        if bss is True:
            scheduler = BackgroundScheduler()
            cur_time = datetime.datetime.now()
            dt = cur_time + datetime.timedelta(minutes=2)
            scheduler.add_job(remove_vlan.remove_vlan, 'date', run_date=dt)
            scheduler.start()
