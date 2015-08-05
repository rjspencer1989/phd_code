from base_doc import BaseDoc
import pprint


class Wifi(BaseDoc):
    def get_rev_list(self):
        revs=[]
        initial_revs = super(Wifi, self).get_rev_list()
        pprint.pprint(initial_revs)
        for rev in initial_revs:
            doc = self.db.get(self.doc['_id'], rev=rev)
            if doc['status'] == 'done':
                revs.append(doc['_rev'])
        return revs

    def undo(self):
        rev_list = self.get_rev_list()
        print rev_list
        doc = self.db.get(self.doc['_id'], rev=rev_list[0])
        doc['status'] = 'pending'
        res = self.db.save_doc(doc, force_update=True)
        return res['rev']
