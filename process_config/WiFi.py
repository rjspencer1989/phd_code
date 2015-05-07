from couchdbkit import *
from Queue import Queue
import threading
from datetime import datetime
import CouchdbConfigParser
from os.path import expanduser
import subprocess
import ChangeNotification

db = CouchdbConfigParser.getDB()
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
                if len(row['value']['service']) > 0 && len(row['value']['name']) > 0:
                    service = row['value']['service']
                    to = row['value']['name']
                    timestr = datetime.now().strftime("%H:%M:%S")
                    ChangeNotification.sendNotification(to, service, "network settings updated at %s" % (timestr))

    def run(self):
        while(True):
            change = self.shared_object.get()
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            current_doc = db.open_doc(the_id, rev=the_rev)
            line_list = []
            line_list.append('interface=wlan0\n')
            line_list.append('driver=nl80211\n')
            line_list.append('ctrl_interface=/var/run/hostapd\n')
            line_list.append('ctrl_interface_group=0\n')
            line_list.append('hw_mode=g\n')
            line_list.append('auth_algs=3\n')
            line_list.append('channel=%s\n' % current_doc['channel'])
            line_list.append('eapol_key_index_workaround=0\n')
            line_list.append('eap_server=0\n')
            line_list.append('own_ip_addr=127.0.0.1\n')
            line_list.append('wep_default_key=0\n')
            line_list.append('ignore_broadcast_ssid=0\n')
            line_list.append('ssid=%s\n' % (current_doc['ssid']))
            if current_doc['password_type'] == 'hex':
                line_list.append('wep_key0=%s\n' % (current_doc['password']))
            else:
                line_list.append('wep_key0=\"%s\"\n' % (current_doc['password']))
            with open('/etc/hostapd/hostapd.conf', 'w') as fh:
                fh.writelines(line_list)
            self.get_connected_devices()
            cmd = ['/etc/init.d/hostapd', 'reload']
            res = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
            try:
                if res.index('done') != -1:
                    current_doc['status'] = 'done'
                    self.notify()
            except ValueError:
                current_doc['status'] = 'error'
            finally:
                db.save_doc(current_doc)
                self.shared_object.task_done()
changeQueue = Queue()
producer = WifiListener("producer", changeQueue)
consumer = WifiProcessor("consumer", changeQueue)
producer.start()
consumer.start()
