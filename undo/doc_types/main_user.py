from base_doc import BaseDoc


class Main_user(BaseDoc):
    def undo(self):
        rev_list = self.get_rev_list()
        prev = self.db.get(self.doc['_id'], rev=rev_list[0])
        self.db.save_doc(prev, force_update=True)
