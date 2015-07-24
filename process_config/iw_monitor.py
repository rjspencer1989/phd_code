#!/usr/bin/env python

import subprocess

result = subprocess.check_output(['iw', 'dev', 'wlan0', 'station', 'dump'])
lines = result.split('\n')
for line in lines:
    if line.startswith('Station'):
        fields = line.split(' ')
        mac_addr = fields[1]
        print mac_addr
