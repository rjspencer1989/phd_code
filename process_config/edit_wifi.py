#!/usr/bin/env python

from couchdbkit import *
from Queue import Queue
import threading
from datetime import datetime
import couchdb_config_parser
import subprocess
import change_notification
import os
import add_history
import pprint

db = couchdb_config_parser.get_db()
db_info = db.info()


class WifiListener(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        changeStream = ChangesStream(db, feed="continuous", heartbeat=True, since=db_info['update_seq'], filter="homework-remote/wifi")
        for change in changeStream:
            self.shared_object.put(change)


class WifiProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue
        self.devices = None

    def get_connected_devices(self):
        vr = db.view('homework-remote/connected_devices')
        self.devices = vr.all()

    def notify(self):
        if self.devices is not None and len(self.devices) > 0:
            for row in self.devices:
                if len(row['value']['notification_service']) > 0 and len(row['value']['name']) > 0:
                    service = row['value']['notification_service']
                    to = row['value']['name']
                    timestr = datetime.now().strftime("%H:%M:%S")
                    change_notification.sendNotification(to, service, "network settings updated at %s" % (timestr))
        return True

    def get_config(self):
        with open('/etc/hostapd/hostapd.conf', 'r') as fh:
            line_list = {}
            lines = fh.readlines()
            for line in lines:
                arr = line.split('=')
                line_list[arr[0]] = line_list[1]
            return line_list

    def generate_config(self, current_doc):
        line_dict = self.get_config()
        print line_dict
        if len(line_dict) > 0 and 'bss' not in line_dict:
            line_dict['channel'] = '%s\n' % (current_doc['channel'])
            if current_doc['mode'] == 'n' and 'ieee80211n' not in line_dict:
                line_dict['ieee80211n'] = '1\n'
            elif current_doc['mode'] == 'g' and 'ieee80211n' in line_dict:
                del line_dict['ieee80211n']
            # line_dict['bss'] = 'wlan0_1\n'
            # line_dict['ssid'] = '%s\n' % (current_doc['ssid'])
            # line_dict['wpa'] = '3\n'
            # line_dict['wpa_passphrase'] = '%s\n' % (current_doc['password'])
            # line_dict['wpa_key_mgmt'] = 'WPA-PSK\n'
            # line_dict['wpa_pairwise'] = 'TKIP\n'
            # line_dict['rsn_pairwise'] = 'CCMP\n'
            line_list = []
            for key, val in line_dict.iteritems():
                line_list.append('='.join((key, val)))
        return line_list

    def run(self):
        while(True):
            change = self.shared_object.get()
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            current_doc = db.open_doc(the_id, rev=the_rev)
            line_list = self.generate_config(current_doc)
            if 'ENV_TESTS' not in os.environ:
                with open('/etc/hostapd/hostapd.conf', 'w') as fh:
                    fh.writelines(line_list)
                self.get_connected_devices()
                current_doc['status'] = 'done'
                db.save_doc(current_doc)
                add_history.add_history_item("New WiFi Configuration", "WiFi configuration has been updated and devices will need to be reconnected", the_id, the_rev, True)
                if self.notify():
                    cmd = ['/etc/init.d/hostapd', 'reload']
                    res = subprocess.Popen(cmd)
changeQueue = Queue()
producer = WifiListener("producer", changeQueue)
consumer = WifiProcessor("consumer", changeQueue)
if 'ENV_TESTS' not in os.environ:
    producer.start()
    consumer.start()
