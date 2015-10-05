from couchdbkit import *
from couchdbkit.changes import ChangesStream
from pox.lib.addresses import EthAddr
from pox.core import core
from pox.lib.revent import Event
from pox.lib.revent.revent import EventMixin
from process_config import couchdb_config_parser
from process_config.add_history import add_history_item


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
        strings = {}
        strings['permit'] = {
            'title': 'Device Permitted',
            'desc': 'Device %s was permitted to access your network' % (device)
        }

        strings['deny'] = {
            'title': 'Device Denied',
            'desc': 'Device %s was denied access to your network' % (device)
        }

        return strings[state]

    def check_device_status(self):
        remote_stream = ChangesStream(self.selected_db, heartbeat=True, since=self.last_seq, filter='homework-remote/devices_pox')
        for change in remote_stream:
            self.last_seq = change['seq']
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            doc = self.selected_db.open_doc(the_id, rev=the_rev)
            prompt = True if ('prompt' in doc and doc['prompt'] == True) else False
            doc_arr = [{'doc_id': the_id, 'doc_rev': the_rev, 'doc_collection': 'devices', 'action': 'edit'}]
            strings = self.get_history_strings(doc['device_name'],
                                               doc['action'])
            add_history_item(strings['title'], strings['desc'],
                             docs=doc_arr,
                             undoable=True,
                             prompt=prompt,
                             ts=doc['event_timestamp'] if 'event_timestamp' in doc else None)
            device = {'mac': EthAddr(doc['mac_address']),
                      'action': doc['action']}
            devices = [device]
            self.raiseEvent(DeviceStateChange(devices))
        core.callDelayed(1, self.check_device_status)


def launch():
    core.registerNew(HomeworkMain)
