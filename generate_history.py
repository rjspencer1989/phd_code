#!/usr/bin/env python
from process_config import couchdb_config_parser
from doc_types import devices, notifications, wifi
import random
import string
import json

db = couchdb_config_parser.get_db()
random.seed(1)
ssid = "homework-%d" % (int(random.getrandbits(25)))
password = ''.join(random.sample(string.printable, 10))
channel = random.choice(range(1,12))
initial_wifi = wifi.Wifi(ssid, password, 'n', channel)
res = db.save_doc(initial_wifi.__dict__)
print res