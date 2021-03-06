#!/usr/bin/env python
import subprocess
import os
from process_config import couchdb_config_parser

db = couchdb_config_parser.get_db()


def reload_hostapd():
    cmd = ['/etc/init.d/hostapd', 'reload']
    res = subprocess.Popen(cmd)


def get_config():
    with open('/etc/hostapd/hostapd.conf') as fh:
        keys = []
        values = []
        lines = fh.readlines()
        for line in lines:
            arr = line.split('=')
            keys.append(arr[0])
            values.append(arr[1].strip())
        return (keys, values)


def remove_vlan_from_switch():
    cmd = ['/usr/local/bin/ovs-vsctl', '--if-exists', 'del-port', 'br0', 'wlan0_1']
    subprocess.call(cmd)


def write_config_file(lines):
    with open('/etc/hostapd/hostapd.conf', 'w') as fh:
        fh.writelines(lines)


def generate_config():
    lines = []
    config = get_config()
    keys = config[0]
    values = config[1]
    if 'bss' in keys:
        bss_index = keys.index('bss')
        new_config_keys = keys[bss_index:]
        new_config_values = values[bss_index:]
        ssid_index = new_config_keys.index('ssid')
        password_index = new_config_keys.index('wpa_passphrase')
        new_ssid = new_config_values[ssid_index]
        new_password = new_config_values[password_index]
        keys[bss_index:] = []
        values[bss_index:] = []
        ssid_index = keys.index('ssid')
        password_index = keys.index('wpa_passphrase')
        values[ssid_index] = new_ssid
        values[password_index] = new_password
        for key, value in zip(keys, values):
            line = '{0}={1}\n'.format(key, value)
            lines.append(line)
    return lines


def remove_vlan():
    doc = db.get('wifi')
    if 'bss_active' in doc and doc['bss_active'] is True:
        doc['bss_active'] = False
        db.save_doc(doc, force_update=True)
    lines = generate_config()
    write_config_file(lines)
    reload_hostapd()
    remove_vlan_from_switch()
