from couchdbkit import *
from couchdbkit.changes import ChangesStream
from pox.lib.addresses import EthAddr
from pox.core import core
from pox.lib.revent import Event
from pox.lib.revent.revent import EventMixin
from process_config import couchdb_config_parser
from process_config import add_history


class DeviceStateChange(Event):
    def __init__(self, devices):
        Event.__init__(self)
        self.devices = devices


class HomeworkMain(EventMixin):
    _eventMixin_events = set([DeviceStateChange])

    def __init__(self):
        self.selected_db = couchdb_config_parser.get_db()
        self.last_seq = self.selected_db.info()['update_seq']
        core.callDelayed(1, self.check_device_status)

    def get_history_strings(self, device, state):
        strings = {
            'permit' : {
                'title': 'Device Permitted',
                'description': 'Device %s was permitted to access your network' % (device)
            }

            'deny' : {
                'title': 'Device Denied',
                'description': 'Device %s was denied access to your network' % (device)
            }
        }

        return strings[state]

    def check_device_status(self):
        remote_stream = ChangesStream(self.selected_db, heartbeat=True, since=self.last_seq, filter='homework-remote/devices_pox')
        for change in remote_stream:
            self.last_seq = change['seq']
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            current_doc = self.selected_db.open_doc(the_id, rev=the_rev)
            history_text = self.get_history_strings(current_doc['device_name'], current_doc['action'])
            add_history.add_history_item(history_text['title'], history_text['description'], the_id, the_rev, False if current_doc['state'] == 'pending' else True)
            device = {'mac': EthAddr(current_doc['mac_address']), 'action': current_doc['action']}
            devices = [device]
            self.raiseEvent(DeviceStateChange(devices))
        core.callDelayed(1, self.check_device_status)


def launch():
    core.registerNew(HomeworkMain)
