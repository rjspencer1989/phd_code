from base_doc import BaseDoc
import pprint

class Devices(BaseDoc):
    def get_rev_list(self):
        revs=[]
        initial_revs = super(Devices, self).get_rev_list()
        for rev in initial_revs:
            doc = self.db.get(self.doc['_id'], rev=rev)
            if doc['changed_by'] == 'user':
                revs.append(doc['_rev'])
        return revs

    def undo(self):
        rev_list = self.get_rev_list()
        doc = self.db.get(self.doc['_id'], rev=rev_list[0])
        self.doc['device_name'] = doc['device_name']
        self.doc['device_type'] = doc['device_type']
        self.doc['name'] = doc['name']
        self.doc['action'] = doc['action']
        res = self.db.save_doc(self.doc)
        return res['rev']
