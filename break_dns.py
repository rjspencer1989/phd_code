#!/usr/bin/env python
from couchdbkit import *
from process_config import couchdb_config_parser
import subprocess
from doc_types import dns

db = couchdb_config_parser.get_db()

lines = []
with open("/etc/dnsmasq.conf", "r") as dh:
    lines = dh.readlines()

if len(lines) > 0:
    lines.append("no-resolv\n")
    with open("/etc/dnsmasq.conf", "w") as dhw:
        dhw.writelines(lines)

dns_doc = dns.DNS()
db.save_doc(dns_doc.get_doc(), force_update=True)

cmd = ["service", "dnsmasq", "restart"]
subprocess.call(cmd)
