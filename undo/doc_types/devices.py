from base_doc import BaseDoc
import pprint

class Devices(BaseDoc):
    def undo(self):
        rev_list = self.get_rev_list()
        pprint.pprint(rev_list)
        return None
