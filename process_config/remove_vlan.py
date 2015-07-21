#!/usr/bin/env python
import subprocess
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
    lines = generate_config()
    write_config_file(lines)
    reload_hostapd()
