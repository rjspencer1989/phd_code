from base_doc import BaseDoc
from process_config import add_history
import subprocess

class Devices(BaseDoc):
    def get_rev_list(self):
        revs=[]
        initial_revs = super(Devices, self).get_rev_list()
        for rev in initial_revs:
            doc = self.db.get(self.doc['_id'], rev=rev)
            if doc['changed_by'] == 'user':
                revs.append(doc['_rev'])
        return revs

    def reload_hostapd(self):
        cmd = ['/etc/init.d/hostapd', 'reload']
        res = subprocess.Popen(cmd)

    def remove_from_hostapd_blacklist(self, mac):
        mac_str = "%s\n" % (mac)
        with open('/etc/hostapd.deny', 'r+') as hsd:
            lines = hsd.readlines()
            if mac_str in lines:
                lines.remove(mac_str)
                hsd.seek(0)
                hsd.writelines(lines)
                hsd.truncate()
        self.reload_hostapd()

    def undo(self):
        rev_list = self.get_rev_list()
        res = ""
        if len(rev_list) > 0:
            doc = self.db.get(self.doc['_id'], rev=rev_list[0])
            self.doc['device_name'] = doc['device_name']
            self.doc['device_type'] = doc['device_type']
            self.doc['name'] = doc['name']
            self.doc['action'] = doc['action']
            self.doc['changed_by'] = 'user'
            res = self.db.save_doc(self.doc, force_update=True)
        else:
            self.doc['_deleted'] = True
            self.remove_from_hostapd_blacklist(self.doc['mac_address'])
            res = self.db.save_doc(self.doc, force_update=True)
            doc_arr = [{'doc_id': self.doc['_id'], 'doc_rev': res['rev'], 'doc_collection': self.doc['collection'], 'action': 'delete'}]
            add_history.add_history_item("Device removed", "%s has been removed" % self.doc['device_name'], doc_arr, undoable=False)

        return res['rev']
