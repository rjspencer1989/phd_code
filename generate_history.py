#!/usr/bin/env python
from process_config import couchdb_config_parser, add_history
from doc_types import *
import random
import string
import datetime
from dateutil.tz import tzutc
import subprocess

db = couchdb_config_parser.get_db()
main_user = main_user.MainUser("", "")
res = db.save_doc(main_user.get_doc(), force_update=True)

ssid = "homework-%d" % (int(random.getrandbits(25)))
password = ''.join(random.sample(string.ascii_lowercase + string.digits, 10))
channel = random.choice(range(1,12))
wifi = wifi.Wifi(ssid, password, 'n', channel)
res = db.save_doc(wifi.get_doc())
wifi.set_field('_id', res['id'])
wifi.set_field('_rev', res['rev'])
print res
dt = datetime.datetime(2014, 01, 12, hour=10, minute=15, tzinfo=tzutc())
add_history.add_history_item("set up wifi", "initial wifi config", res["id"], res["rev"], False, dt.isoformat())

aspire = devices.Device("d0:27:88:80:d9:ef", "10.2.0.1", "aspire", "eth1", state="permit")
res = db.save_doc(aspire.get_doc(), force_update=True)
dt = datetime.datetime(2014, 01, 12, hour=10, minute=20, tzinfo=tzutc())
add_history.add_history_item("Device Permitted", "Device was permitted to access your network", res["id"], res["rev"], False, dt.isoformat())

aspire.set_field("device_name", "aspire")
aspire.set_field("notification_service", "phone")
aspire.set_field("name", "John")
aspire.set_field("device_type", "desktop")
res = db.save_doc(aspire.get_doc(), force_update=True)
dt = datetime.datetime(2014, 01, 12, hour=10, minute=21, tzinfo=tzutc())
add_history.add_history_item("Device Edited", "Device  Aspire was edited", res["id"], res["rev"], True, dt.isoformat())

main_user.set_field("name", "John")
main_user.set_field("service", "phone")
res=db.save_doc(main_user.get_doc(), force_update=True)

dt = datetime.datetime(2014, 01, 12, hour=10, minute=21, tzinfo=tzutc())
add_history.add_history_item("Added main user", "Added John as main user for receiving network notifications", res["id"], res["rev"], True, dt.isoformat())

john_phone = notifications.Notification("John", "phone", "+447972058628")
res = db.save_doc(john_phone.get_doc(), force_update=True)
dt = datetime.datetime(2014, 01, 12, hour=10, minute=22, tzinfo=tzutc())
add_history.add_history_item("New Notification Registration", "Added +447972058628 as phone number for John", res["id"], res["rev"], True, dt.isoformat())

callison = devices.Device("00:13:77:e1:d2:41", "10.2.0.5", "CALLISON", "eth2")
res = db.save_doc(callison.get_doc(), force_update=True)

callison.set_field("device_name", "callison")
callison.set_field("notification_service", "email")
callison.set_field("name", "Mary")
callison.set_field("device_type", "laptop")
callison.set_field("state", "permit")
res = db.save_doc(callison.get_doc(), force_update=True)
dt = datetime.datetime(2014, 01, 12, hour=10, minute=31, tzinfo=tzutc())
add_history.add_history_item("Device permitted", "callison was permitted to access your network", res["id"], res["rev"], False, dt.isoformat())

mrldesx2 = devices.Device("a0:f4:50:f3:48:50", "10.2.0.9", "android-aa474646cd34eeaa", "wlan0")
res = db.save_doc(mrldesx2.get_doc(), force_update=True)

mrldesx2.set_field("device_name", "mrldesx2")
mrldesx2.set_field("notification_service", "twitter")
mrldesx2.set_field("name", "John")
mrldesx2.set_field("device_type", "phone")
mrldesx2.set_field("state", "permit")
res = db.save_doc(mrldesx2.get_doc(), force_update=True)
dt = datetime.datetime(2014, 01, 12, hour=11, minute=1, tzinfo=tzutc())
add_history.add_history_item("Device Permitted", "mrldesx2 is permitted to access your network", res["id"], res["rev"], False, dt.isoformat())

iphone = devices.Device("40:d3:2d:e3:92:d2", "10.2.0.13", "iPhone", "wlan0")
res = db.save_doc(iphone.get_doc(), force_update=True)

iphone.set_field("device_name", "iphone")
iphone.set_field("notification_service", "phone")
iphone.set_field("name", "Mary")
iphone.set_field("device_type", "phone")
iphone.set_field("state", "permit")
res = db.save_doc(iphone.get_doc(), force_update=True)
dt = datetime.datetime(2014, 01, 12, hour=19, minute=35, tzinfo=tzutc())
add_history.add_history_item("Device Permitted", "iphone is permitted to access your network", res["id"], res["rev"], False, dt.isoformat())

camera = devices.Device("20:13:e0:d7:a1:36", "10.2.0.17", "DHCP-Thread", "wlan0")
res = db.save_doc(camera.get_doc(), force_update=True)

camera.set_field("device_name", "Camera")
camera.set_field("notification_service", "email")
camera.set_field("name", "everyone")
camera.set_field("device_type", "other")
camera.set_field("state", "permit")
res = db.save_doc(camera.get_doc(), force_update=True)
dt = datetime.datetime(2014, 07, 25, hour=18, minute=25, tzinfo=tzutc())
add_history.add_history_item("Device Permitted", "Camera was permitted to access your network", res["id"], res["rev"], False, dt.isoformat())

mrltablet6 = devices.Device("e0:b9:a5:8c:45:cd", "10.2.0.21", "android_8a0b6f3a084dc84a", "wlan0")
res = db.save_doc(mrltablet6.get_doc(), force_update=True)

mrltablet6.set_field("device_name", "mrltablet6")
mrltablet6.set_field("notification_service", "twitter")
mrltablet6.set_field("name", "Mary")
mrltablet6.set_field("device_type", "tablet")
mrltablet6.set_field("state", "permit")
res = db.save_doc(mrltablet6.get_doc(), force_update=True)
dt = datetime.datetime(2014, 12, 27, hour=13, minute=0, tzinfo=tzutc())
add_history.add_history_item("Device Permitted", "mrltablet6 was permitted to access your network", res["id"], res["rev"], False, dt.isoformat())

bad_ipod = devices.Device("c8:b5:b7:5d:f4:ab", "10.2.0.25", "iPod", "wlan0")
res = db.save_doc(bad_ipod.get_doc(), force_update=True)

bad_ipod.set_field("device_name", "bad ipod")
bad_ipod.set_field("state", "deny")
res = db.save_doc(bad_ipod.get_doc(), force_update=True)
dt = datetime.datetime(2015, 01, 29, hour=19, minute=12, tzinfo=tzutc())
add_history.add_history_item("Device Denied", "bad ipod was denied from accessing your network", res["id"], res["rev"], False, dt.isoformat())

wifi.set_field("ssid", "john_and_mary")
wifi.set_field("password", "whatever")
res = db.save_doc(wifi.get_doc(), force_update=True)
print res
dt = datetime.datetime(2015, 01, 30, hour=19, minute=0, tzinfo=tzutc())
add_history.add_history_item("Wifi settings updated", "Wifi configuration has been updated and you need to reconnect your devices", res["id"], res["rev"], True, dt.isoformat())

rjsxperia1 = devices.Device("a0:e4:53:55:00:cc", "10.2.0.29", "android-5f251018c8685b52", "wlan0")
res = db.save_doc(rjsxperia1.get_doc(), force_update=True)

rjsxperia1.set_field("device_name", "rjsxperia1")
rjsxperia1.set_field("notification_service", "phone")
rjsxperia1.set_field("name", "John")
rjsxperia1.set_field("device_type", "phone")
rjsxperia1.set_field("state", "permit")
res = db.save_doc(rjsxperia1.get_doc(), force_update=True)
dt = datetime.datetime(2015, 07, 20, hour=19, minute=30, tzinfo=tzutc())
add_history.add_history_item("Device Permitted", "rjsxperia1 was permitted to access your network", res["id"], res["rev"], False, dt.isoformat())

john_email = notifications.Notification("John", "email", "rob@robspencer.me.uk")
res = db.save_doc(john_email.get_doc(), force_update=True)
dt = datetime.datetime(2014, 07, 25, hour=18, minute=30, tzinfo=tzutc())
add_history.add_history_item("New Notification Registration", "Added rob@robspencer.me.uk as email address for John", res["id"], res["rev"], True, dt.isoformat())

john_twitter = notifications.Notification("John", "twitter", "rjspencer1989")
res = db.save_doc(john_twitter.get_doc(), force_update=True)
dt = datetime.datetime(2014, 01, 12, hour=11, minute=02, tzinfo=tzutc())
add_history.add_history_item("New Notification Registration", "Added rjspencer1989 as twitter username for John", res["id"], res["rev"], True, dt.isoformat())

mary_email = notifications.Notification("Mary", "email", "rob@robspencer.me.uk")
res = db.save_doc(mary_email.get_doc(), force_update=True)
dt = datetime.datetime(2014, 01, 12, hour=10, minute=32, tzinfo=tzutc())
add_history.add_history_item("New Notification Registration", "Added rob@robspencer.me.uk as email address for Mary", res["id"], res["rev"], True, dt.isoformat())

mary_phone = notifications.Notification("Mary", "phone", "+447972058628")
res = db.save_doc(mary_phone.get_doc(), force_update=True)
dt = datetime.datetime(2014, 01, 12, hour=19, minute=36, tzinfo=tzutc())
add_history.add_history_item("New Notification Registration", "Added +447972058628 as phone number for Mary", res["id"], res["rev"], True, dt.isoformat())

mary_twitter = notifications.Notification("Mary", "twitter", "rjspencer1989")
res = db.save_doc(mary_twitter.get_doc(), force_update=True)
dt = datetime.datetime(2014, 12, 27, hour=13, minute=01, tzinfo=tzutc())
add_history.add_history_item("New Notification Registration", "Added rjspencer1989 as twitter username for Mary", res["id"], res["rev"], True, dt.isoformat())

cmd = ['/usr/sbin/service', 'homework-pox', 'start']
res = subprocess.Popen(cmd)