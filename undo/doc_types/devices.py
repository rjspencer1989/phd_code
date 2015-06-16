from base_doc import BaseDoc
import pprint

class Devices(BaseDoc):
    def get_rev_list(self):
        revs=[]
        initial_revs = super(Devices, self).get_rev_list()
        for rev in initial_revs:
            doc = self.db.get(self.doc['_id'], rev=rev)
            if doc['changed_by'] == 'user':
                revs.append(rev)

    def undo(self):
        rev_list = self.get_rev_list()
        pprint.pprint(rev_list)
        return self.doc['_rev']
