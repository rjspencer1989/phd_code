from base_doc import BaseDoc

class Dns(BaseDoc):
    def get_rev_list(self):
        rl = super(Dns, self)
        return rl

    def undo(self):
        rev_list = self.get_rev_list()
        res = self.db.save_doc(self.doc, force_update=True)
        return res
