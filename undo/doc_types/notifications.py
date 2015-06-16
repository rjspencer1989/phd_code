from process_config import notification_registration_client
from base_doc import BaseDoc
import pprint

class Notifications(BaseDoc):
    def undo(self):
        rev_list = self.get_rev_list()
        pprint.pprint(rev_list)
        result = ''
        if len(rev_list) == 0:
            result = self.undo_new()
        elif 'hidden' in self.doc:
            result = self.undo_delete()
        else:
            result = self.undo_edit()
        return result

    def undo_new(self):
        self.doc['hidden'] = True
        ret = self.db.save_doc(self.doc)
        hidden = self.db.get(self.doc['_id'], rev=ret['rev'])
        notification_registration_client.delete(hidden)
        updated = self.db.get(self.doc['_id'])
        return updated['_rev']

    def undo_delete(self):
        del self.doc['hidden']
        self.doc['status'] = 'done'
        self.db.save_doc(self.doc, force_update=True)
        notification_registration_client.registration(self.doc)
        updated = self.db.get(self.doc['_id'])
        return updated['_rev']

    def undo_edit(self):
        rev_list = self.get_rev_list()
        prev = self.db.get(self.doc['_id'], rev_list[0])
        pprint.pprint(prev)
        return prev['_rev']
