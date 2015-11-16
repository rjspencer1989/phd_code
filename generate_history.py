#!/usr/bin/env python
from process_config import couchdb_config_parser, add_history
from doc_types import *
import random
import string
import datetime
from dateutil.tz import tzutc
import subprocess
import pprint
import time

db = couchdb_config_parser.get_db()
main_user = main_user.MainUser("", "")
res = db.save_doc(main_user.get_doc(), force_update=True)

connection_state = connection_state.ConnectionState()
res = db.save_doc(connection_state.get_doc(), force_update=True)
random.seed(1)
ssid = "homework-%d" % (int(random.getrandbits(25)))
password = ''.join(random.sample(string.ascii_lowercase + string.digits, 10))
channel = random.choice(range(1,12))
dt = datetime.datetime(2014, 01, 12, hour=10, minute=15, tzinfo=tzutc())
wifi = wifi.Wifi(ssid, password, 'n', channel, timestamp=dt.isoformat())
res = db.save_doc(wifi.get_doc(), force_update=True)
wifi.set_field('_rev', res['rev'])

dt = datetime.datetime(2014, 01, 12, hour=10, minute=20, tzinfo=tzutc())
ballard = devices.Device("00:27:0e:30:22:5d", "10.2.0.1", "ballard", "eth1", timestamp=dt.isoformat())
ballard.set_field("device_name", "John's Computer")
ballard.set_field("notification_service", "phone")
ballard.set_field("name", "John")
ballard.set_field("device_type", "desktop")
ballard.set_field("changed_by", "user")
ballard.set_field("action", "permit")
dt = datetime.datetime(2014, 01, 12, hour=10, minute=21, tzinfo=tzutc())
ballard.set_field("event_timestamp", dt.isoformat())
res = db.save_doc(ballard.get_doc(), force_update=True)

main_user.set_field("name", "John")
main_user.set_field("service", "phone")
main_user.set_field("status", "pending")
dt = datetime.datetime(2014, 01, 12, hour=10, minute=21, tzinfo=tzutc())
main_user.set_field("event_timestamp", dt.isoformat())
res=db.save_doc(main_user.get_doc(), force_update=True)

dt = datetime.datetime(2014, 01, 12, hour=10, minute=22, tzinfo=tzutc())
john_phone = notifications.Notification("John", "phone", "+447523221070", timestamp=dt.isoformat())
res = db.save_doc(john_phone.get_doc(), force_update=True)

callison = devices.Device("00:13:77:e1:d2:41", "10.2.0.5", "CALLISON", "eth2")
res = db.save_doc(callison.get_doc(), force_update=True)

callison.set_field("device_name", "Mary's Laptop")
callison.set_field("notification_service", "email")
callison.set_field("name", "Mary")
callison.set_field("device_type", "laptop")
callison.set_field("changed_by", "user")
callison.set_field("action", "permit")
dt = datetime.datetime(2014, 01, 12, hour=10, minute=31, tzinfo=tzutc())
callison.set_field("event_timestamp", dt.isoformat())
res = db.save_doc(callison.get_doc(), force_update=True)

mrldesx2 = devices.Device("a0:f4:50:f3:48:50", "10.2.0.9", "android-aa474646cd34eeaa", "wlan0")
res = db.save_doc(mrldesx2.get_doc(), force_update=True)

mrldesx2.set_field("device_name", "Mary's Phone")
mrldesx2.set_field("notification_service", "email")
mrldesx2.set_field("name", "Mary")
mrldesx2.set_field("device_type", "phone")
mrldesx2.set_field("action", "permit")
mrldesx2.set_field("changed_by", "user")
dt = datetime.datetime(2014, 01, 12, hour=11, minute=00, tzinfo=tzutc())
mrldesx2.set_field("event_timestamp", dt.isoformat())
res = db.save_doc(mrldesx2.get_doc(), force_update=True)

iphone = devices.Device("40:d3:2d:e3:92:d2", "10.2.0.13", "johns_iphone", "wlan0")
res = db.save_doc(iphone.get_doc(), force_update=True)

iphone.set_field("device_name", "John's iPhone")
iphone.set_field("notification_service", "phone")
iphone.set_field("name", "John")
iphone.set_field("device_type", "phone")
iphone.set_field("action", "permit")
iphone.set_field("changed_by", "user")
dt = datetime.datetime(2014, 01, 12, hour=19, minute=35, tzinfo=tzutc())
iphone.set_field("event_timestamp", dt.isoformat())
res = db.save_doc(iphone.get_doc(), force_update=True)

xbox = devices.Device("30:59:b7:48:bc:39", "10.2.0.21", "Xbox-SystemOS", "wlan0")
res = db.save_doc(xbox.get_doc(), force_update=True)

xbox.set_field("device_name", "XBOX One")
xbox.set_field("notification_service", "phone")
xbox.set_field("name", "John")
xbox.set_field("device_type", "other")
xbox.set_field("action", "permit")
xbox.set_field("changed_by", "user")
dt = datetime.datetime(2014, 07, 25, hour=18, minute=25, tzinfo=tzutc())
xbox.set_field("event_timestamp", dt.isoformat())
res = db.save_doc(xbox.get_doc(), force_update=True)

mrltablet6 = devices.Device("e0:b9:a5:8c:45:cd", "10.2.0.17", "android_8a0b6f3a084dc84a", "wlan0")
res = db.save_doc(mrltablet6.get_doc(), force_update=True)

mrltablet6.set_field("device_name", "Mary's Tablet")
mrltablet6.set_field("notification_service", "email")
mrltablet6.set_field("name", "Mary")
mrltablet6.set_field("device_type", "tablet")
mrltablet6.set_field("action", "permit")
mrltablet6.set_field("changed_by", "user")
dt = datetime.datetime(2014, 12, 27, hour=13, minute=0, tzinfo=tzutc())
mrltablet6.set_field("event_timestamp", dt.isoformat())
res = db.save_doc(mrltablet6.get_doc(), force_update=True)

dt = datetime.datetime(2014, 01, 12, hour=10, minute=32, tzinfo=tzutc())
mary_email = notifications.Notification("Mary", "email", "psxrjs-demo@outlook.com", timestamp=dt.isoformat())
res = db.save_doc(mary_email.get_doc(), force_update=True)

time.sleep(10)
updated = db.get(mrldesx2.mac_address)
mrldesx2.set_field("state", updated["state"])
mrldesx2.set_field("action", "deny")
mrldesx2.set_field("changed_by", "user")
dt = datetime.datetime(2015, 10, 25, hour=15, minute=20, tzinfo=tzutc())
mrldesx2.set_field("event_timestamp", dt.isoformat())
res = db.save_doc(mrldesx2.get_doc(), force_update=True)

ports = ["eth1", "eth2", "eth3"]
for port in ports:
    cmd = ["ifup", port]
    subprocess.call(cmd)

cmd = ["/etc/init.d/hostapd", "start"]
subprocess.call(cmd)
