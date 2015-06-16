from base_doc import BaseDoc
import pprint

class Devices(BaseDoc):
    def undo(self):
        pprint.pprint(self.doc)
        return self.doc['_rev']
