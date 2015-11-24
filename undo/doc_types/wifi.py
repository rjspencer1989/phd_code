from base_doc import BaseDoc
from process_config import edit_wifi
import pprint


class Wifi(BaseDoc):
    def get_rev_list(self):
        revs=[]
        initial_revs = super(Wifi, self).get_rev_list()
        for rev in initial_revs:
            doc = self.db.get(self.doc['_id'], rev=rev)
            if doc['status'] == 'done':
                revs.append(doc['_rev'])
        return revs

    def undo(self):
        rev_list = self.get_rev_list()
        doc = self.db.get(self.doc['_id'], rev=rev_list[0])
        if doc['bss_active'] is True:
            print "bss active\n"
            doc['bss_active'] = False
            doc['with_bss'] = False
        pprint.pprint(doc)

        res = self.db.save_doc(doc, force_update=True)
        doc = self.db.get(self.doc['_id'])
        edit_wifi.process_wifi(doc, from_undo=True)
        return res['rev']
