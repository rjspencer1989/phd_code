from base_doc import BaseDoc


class Wifi(BaseDoc):
    def undo(self):
        print self.doc
        return self.doc['_rev']
