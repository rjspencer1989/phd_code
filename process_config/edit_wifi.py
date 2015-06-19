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

    def generate_config(self, current_doc):
        line_list = []
        line_list.append('interface=wlan0\n')
        line_list.append('bridge=br0\n')
        line_list.append('driver=nl80211\n')
        line_list.append('logger_syslog=-1\n')
        line_list.append('logger_syslog_level=2\n')
        line_list.append('logger_stdout=-1\n')
        line_list.append('logger_stdout_level=2\n')
        line_list.append('debug=0\n')
        line_list.append('dump_file=/tmp/hostapd.dump\n')
        line_list.append('ctrl_interface=/var/run/hostapd\n')
        line_list.append('ctrl_interface_group=0\n')
        line_list.append('ssid=%s\n' % (current_doc['ssid']))
        line_list.append('hw_mode=g\n')
        line_list.append('channel=%s\n' % current_doc['channel'])
        if current_doc['mode'] == 'n':
            line_list.append('ieee80211n=1\n')
        line_list.append('beacon_int=100\n')
        line_list.append('dtim_period=2\n')
        line_list.append('max_num_sta=255\n')
        line_list.append('rts_threshold=2347\n')
        line_list.append('fragm_threshold=2346\n')
        line_list.append('macaddr_acl=0\n')
        line_list.append('auth_algs=1\n')
        line_list.append('ignore_broadcast_ssid=0\n')
        line_list.append('eapol_key_index_workaround=0\n')
        line_list.append('eap_server=0\n')
        line_list.append('own_ip_addr=127.0.0.1\n')
        line_list.append('wpa_passphrase=%s\n' % (current_doc['password']))
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
                    cmd = ['/sbin/reboot']
                    res = subprocess.Popen(cmd)
changeQueue = Queue()
producer = WifiListener("producer", changeQueue)
consumer = WifiProcessor("consumer", changeQueue)
if 'ENV_TESTS' not in os.environ:
    producer.start()
    consumer.start()
