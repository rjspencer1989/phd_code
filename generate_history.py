#!/usr/bin/env python
from process_config import couchdb_config_parser, add_history
from doc_types import devices, main_user, notifications, wifi
import random
import string
import datetime
from dateutil.tz import tzutc

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
dt = datetime.datetime(2014, 01, 12, hour=10, minute=15, tzinfo=tzutc())
add_history.add_history_item("set up wifi", "initial wifi config", res["id"], res["rev"], False, dt.isoformat())

mrldesx2 = devices.Devices("a0:f4:50:f3:48:50", "10.2.0.5", "android-a1", "", "", "add", "", "pending", "", "wlan0")
res = db.save_doc(mrldesx2.get_doc(), force_update=True)
print res

rjsxperia1 = devices.Devices("a0:e4:53:55:00:cc", "10.2.0.33", "android-a2", "", "", "add", "", "pending", "", "wlan0")
res = db.save_doc(rjsxperia1.get_doc(), force_update=True)
print res

mrltablet6 = devices.Devices("e0:b9:a5:8c:45:cd", "10.2.0.29", "android-a3", "", "", "add", "", "pending", "", "wlan0")
res = db.save_doc(mrltablet6.get_doc(), force_update=True)
print res

john_email = notifications.Notifications("John", "email", "rob@robspencer.me.uk")
res = db.save_doc(john_email.get_doc(), force_update=True)
print res

john_phone = notifications.Notifications("John", "phone", "+447972058628")
res = db.save_doc(john_phone.get_doc(), force_update=True)
print res

john_twitter = notifications.Notifications("John", "twitter", "rjspencer1989")
res = db.save_doc(john_twitter.get_doc(), force_update=True)
