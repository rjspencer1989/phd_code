#!/usr/bin/env python
from process_config import couchdb_config_parser, add_history
from doc_types import *
import random
import string
import datetime
from dateutil.tz import tzutc

db = couchdb_config_parser.get_db()
db.flush()
main_user = main_user.MainUser("", "")
res = db.save_doc(main_user.get_doc(), force_update=True)
print res

ssid = "homework-%d" % (int(random.getrandbits(25)))
password = ''.join(random.sample(string.ascii_lowercase + string.digits, 10))
channel = random.choice(range(1,12))
initial_wifi = wifi.Wifi(ssid, password, 'n', channel)
res = db.save_doc(initial_wifi.get_doc())
dt = datetime.datetime(2014, 01, 12, hour=10, minute=15, tzinfo=tzutc())
add_history.add_history_item("set up wifi", "initial wifi config", res["id"], res["rev"], False, dt.isoformat())

aspire = devices.Device("d0:27:88:80:d9:ef", "10.2.0.1", "aspire", "eth1")
res = db.save_doc(aspire.get_doc(), force_update=True)
print res

main_user.set_field("name", "John")
main_user.set_field("service", "phone")

john_phone = notifications.Notification("John", "phone", "+447972058628")
res = db.save_doc(john_phone.get_doc(), force_update=True)
print res

mrldesx2 = devices.Device("a0:f4:50:f3:48:50", "10.2.0.5", "android-aa474646cd34eeaa", "wlan0")
res = db.save_doc(mrldesx2.get_doc(), force_update=True)
print res

rjsxperia1 = devices.Device("a0:e4:53:55:00:cc", "10.2.0.9", "android-5f251018c8685b52", "wlan0")
res = db.save_doc(rjsxperia1.get_doc(), force_update=True)
print res

mrltablet6 = devices.Device("e0:b9:a5:8c:45:cd", "10.2.0.13", "android_8a0b6f3a084dc84a", "wlan0")
res = db.save_doc(mrltablet6.get_doc(), force_update=True)
print res

callison = devices.Device("00:13:77:e1:d2:41", "10.2.0.17", "CALLISON", "eth2")
res = db.save_doc(callison.get_doc(), force_update=True)
print res

camera = devices.Device("20:13:e0:d7:a1:36", "10.2.0.21", "DHCP-Thread", "wlan0")
res = db.save_doc(camera.get_doc(), force_update=True)
print res

iphone = devices.Device("40:d3:2d:e3:92:d2", "10.2.0.25", "iPhone", "wlan0")
res = db.save_doc(iphone.get_doc(), force_update=True)
print res

john_email = notifications.Notification("John", "email", "rob@robspencer.me.uk")
res = db.save_doc(john_email.get_doc(), force_update=True)
print res

john_twitter = notifications.Notification("John", "twitter", "rjspencer1989")
res = db.save_doc(john_twitter.get_doc(), force_update=True)
print res

mary_email = notifications.Notification("Mary", "email", "rob@robspencer.me.uk")
res = db.save_doc(mary_email.get_doc(), force_update=True)
print res

mary_phone = notifications.Notification("Mary", "phone", "+447972058628")
res = db.save_doc(john_phone.get_doc(), force_update=True)
print res

mary_twitter = notifications.Notification("mary", "twitter", "rjspencer1989")
res = db.save_doc(john_twitter.get_doc(), force_update=True)
print res
