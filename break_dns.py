#!/usr/bin/env python
from couchdbkit import *
from process_config import couchdb_config_parser
import subprocess

db = couchdb_config_parser.get_db()

lines = []
with open("/etc/dnsmasq.conf", "r") as dh:
    lines = dh.readlines()

if len(lines) > 0:
    lines.append("no-resolv\n")
    with open("/etc/dnsmasq.conf", "w") as dhw:
        dhw.writelines(lines)

cmd = ["service", "dnsmasq", "restart"]
subprocess.call(cmd)
