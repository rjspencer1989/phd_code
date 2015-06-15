from process_config import couchdb_config_parser
from base_doc import BaseDoc

class Notifications(BaseDoc):
    def undo(self):
        print 'boo'
