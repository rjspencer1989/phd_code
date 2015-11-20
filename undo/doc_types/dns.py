from base_doc import BaseDoc

class Dns(BaseDoc):
    def get_rev_list(self):
        rl = super(Dns, self)
        rev_list = []
        for rev in rl:
            doc = self.db.get(self.doc['_id'], rev=rev)
            if doc['status'] == "done":
                rev_list.append(rev)
        return rev_list

    def undo(self):
        rev_list = self.get_rev_list()
        if len(rev_list) == 0:
            return None
        rev = rev_list[0]
        doc = self.db.get(self.doc['_id'], rev=rev)
        self.doc = doc
        res = self.db.save_doc(self.doc, force_update=True)
        return res
