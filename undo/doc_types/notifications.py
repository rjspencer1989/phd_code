from process_config import notification_registration_client
from base_doc import BaseDoc
import pprint


class Notifications(BaseDoc):
    def undo(self):
        pprint.pprint(self.doc)
        rev_list = self.get_rev_list()
        result = ''
        if self.action == 'add':
            result = self.undo_new()
        elif self.action == 'delete':
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
        prev = self.db.get(self.doc['_id'], rev=rev_list[0])
        self.doc['user'] = prev['user']
        ret = self.db.save_doc(self.doc)
        mod = self.db.get(self.doc['_id'], rev=ret['rev'])
        notification_registration_client.edit(mod)
        updated = self.db.get(self.doc['_id'])
        return updated['_rev']
