#!/usr/bin/env

import subprocess

result = subprocess.check_output(['iw', 'dev', 'wlan0', 'station', 'dump'])
lines = result.split('\n')
print lines
