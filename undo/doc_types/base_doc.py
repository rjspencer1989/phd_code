from process_config import couchdb_config_parser


class BaseDoc(object):
    def __init__(self, doc, event):
        self.doc = doc
        self.evt = event
        if len(event['docs']) == 1:
            self.current_rev = event['docs'][0]['doc_rev']
            self.action = event['docs'][0]['action']
        self.db = couchdb_config_parser.get_db()

    def get_rev_list(self):
        revs_info = self.doc['_revs_info']
        rev_list = []
        for item in revs_info:
            rev_list.append(str(item['rev']))
        current_index = rev_list.index(self.current_rev)
        revs_list = rev_list[current_index + 1:]
        return revs_list
