#!/usr/bin/env python
from process_config import couchdb_config_parser
from doc_types import devices, main_user, notifications, wifi
import random
import string

db = couchdb_config_parser.get_db()
db.flush()
random.seed(2)
main_user = main_user.MainUser("", "")
res = db.save_doc(main_user.get_doc(), force_update=True)
print res
ssid = "homework-%d" % (int(random.getrandbits(25)))
password = ''.join(random.sample(string.printable, 10))
channel = random.choice(range(1,12))
initial_wifi = wifi.Wifi(ssid, password, 'n', channel)
res = db.save_doc(initial_wifi.get_doc())
print res

mrldesx2 = devices.Devices("a0:f4:50:f3:48:50", "10.2.0.1", "mrldesx2", "John", "add", "phone", "permit", "email", "wlan0")
res = db.save_doc(mrldesx2.get_doc(), force_update=True)
print res

rjsxperia1 = devices.Devices("a0:e4:53:55:00:cc", "10.2.0.5", "rjsxperia1", "Mary", "add", "phone", "permit", "phone", "wlan0")
res = db.save_doc(rjsxperia1.get_doc(), force_update=True)
print res

mrltablet6 = devices.Devices("e0:b9:a5:8c:45:cd", "10.2.0.9", "mrltablet6", "John", "add", "tablet", "permit", "email", "wlan0")
res = db.save_doc(mrltablet6.get_doc(), force_update=True)
print res
