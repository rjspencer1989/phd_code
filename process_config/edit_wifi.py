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
            keys = []
            values = []
            lines = fh.readlines()
            for line in lines:
                arr = line.split('=')
                keys.append(arr[0])
                values.append(arr[1])
            return (keys, values)

    def generate_config(self, current_doc):
        line_list = self.get_config()
        keys = line_list[0]
        values = line_list[1].strip()
        lines = []
        print keys
        if len(keys) > 0 and 'bss' not in keys:
            channel_index = keys.index('channel')
            values[channel_index] = current_doc['channel']
            if current_doc['mode'] == 'n' and 'ieee80211n' not in keys:
                keys.append('ieee80211n')
                values.append('1\n')
            elif current_doc['mode'] == 'g' and 'ieee80211n' in keys:
                n_index = keys.index('ieee80211n')
                keys.pop(n_index)
                values.pop(n_index)
            for key, value in zip(keys, values):
                line = '{0}={1}\n'.format(key, value)
                lines.append(line)
            # line_list['bss'] = 'wlan0_1\n'
            # line_list['ssid'] = '%s\n' % (current_doc['ssid'])
            # line_list['wpa'] = '3\n'
            # line_list['wpa_passphrase'] = '%s\n' % (current_doc['password'])
            # line_list['wpa_key_mgmt'] = 'WPA-PSK\n'
            # line_list['wpa_pairwise'] = 'TKIP\n'
            # line_list['rsn_pairwise'] = 'CCMP\n'
        return lines

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
