#!/usr/bin/env python

from couchdbkit import *
from Queue import Queue
import threading
from datetime import datetime
import couchdb_config_parser
import subprocess
import change_notification
import os
import add_history
import pprint

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
                timestr = datetime.now().strftime("%H:%M:%S")
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
    cmd = ['/etc/init.d/hostapd', 'reload']
    res = subprocess.Popen(cmd)


def generate_config(current_doc):
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
        for key, value in zip(keys, values):
            line = '{0}={1}\n'.format(key, value)
            lines.append(line)

        if 'bss' in keys:
            bss_index = keys.index('bss')
            keys = keys[0:bss_index]
            values = values[0:bss_index]
        lines.append('bss=wlan0_1\n')
        lines.append('ssid=%s\n' % (current_doc['ssid']))
        lines.append('wpa=3\n')
        lines.append('wpa_passphrase=%s\n' % (current_doc['password']))
        lines.append('wpa_key_mgmt=WPA-PSK\n')
        lines.append('wpa_pairwise=TKIP\n')
        lines.append('rsn_pairwise=CCMP')
    return lines


def process_wifi(doc):
    line_list = generate_config(doc)
    write_config_file(line_list)
    devices = get_connected_devices()
    doc['status'] = 'done'
    db.save_doc(doc)
    title = "New WiFi Configuration"
    desc = "WiFi configuration has been updated. "
    desc += "You will need to reconnect your devices"
    add_history.add_history_item(title, desc, doc['_id'], doc['_rev'], True)
    if notify(devices):
        reload_hostapd()
