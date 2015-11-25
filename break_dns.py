#!/usr/bin/env python
from couchdbkit import *
from process_config import couchdb_config_parser
import subprocess
from doc_types import dns
from datetime import datetime, timedelta
from dateutil.tz import tzutc

db = couchdb_config_parser.get_db()

lines = []
with open("/etc/dnsmasq.conf", "r") as dh:
    lines = dh.readlines()

dns_doc = db.get("dns")
dns_doc["dns_status"] = "error"
dns_doc["status"] = "pending"
db.save_doc(dns_doc, force_update=True)

if len(lines) > 0 and "no-resolv\n" not in lines:
    lines.append("no-resolv\n")
    with open("/etc/dnsmasq.conf", "w") as dhw:
        dhw.writelines(lines)

    cmd = ["/etc/init.d/dnsmasq", "restart"]
    subprocess.call(cmd)
