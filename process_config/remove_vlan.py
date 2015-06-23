#!/usr/bin/env python
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
