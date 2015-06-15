from process_config import couchdb_config_parser


class BaseDoc(object):
    def __init__(self, doc, current_rev):
        self.doc = doc
        self.current_rev = current_rev
        self.db = couchdb_config_parser.get_db()

    def get_rev_list(self):
        revs_info = self.doc['_revs_info']
        rev_list = []
        for item in revs_info:
            rev_list.append(str(item['rev']))
        current_index = rev_list.index(self.current_rev)
        revs_list = rev_list[current_index + 1:]
        return revs_list
