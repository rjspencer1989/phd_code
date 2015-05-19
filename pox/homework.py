from couchdbkit import Server
import ConfigParser
from os.path import expanduser
from couchdbkit.changes import ChangesStream
from pox.lib.addresses import EthAddr
from pox.core import core
from pox.lib.revent import Event
from pox.lib.revent.revent import EventMixin


class DeviceStateChange(Event):
    def __init__(self, devices):
        Event.__init__(self)
        self.devices = devices


class HomeworkMain(EventMixin):
    _eventMixin_events = set([DeviceStateChange])

    def __init__(self):
        cp = ConfigParser.ConfigParser()
        path = "/home/homeuser/couchdb.conf"
        cp.read(path)
        couchdb_server = cp.get('DEFAULT', 'SERVER_NAME')
        couchdb_port = cp.get('DEFAULT', 'PORT')
        couchdb_db = cp.get('DEFAULT', 'DB')
        couchdb_admin = cp.get('DEFAULT', 'ADMIN')
        couchdb_admin_password = cp.get('DEFAULT', 'ADMIN_PASSWORD')
        couchdb_url = "http://%s:%s@%s:%s" % (couchdb_admin, couchdb_admin_password, couchdb_server, couchdb_port)

        self.server = Server(couchdb_url)
        self.selected_db = self.server[couchdb_db]
        self.last_seq = self.selected_db.info()['update_seq']
        core.callDelayed(1, self.check_device_status)

    def check_device_status(self):
        remote_stream = ChangesStream(self.selected_db, heartbeat=True, since=self.last_seq, filter='homework-remote/devices_pox')
        for change in remote_stream:
            self.last_seq = change['seq']
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            current_doc = self.selected_db.open_doc(the_id, rev=the_rev)
            device = {'mac': EthAddr(current_doc['mac_address']), 'action': current_doc['action']}
            devices = [device]
            self.raiseEvent(DeviceStateChange(devices))
        core.callDelayed(1, self.check_device_status)


def launch():
    core.registerNew(HomeworkMain)
