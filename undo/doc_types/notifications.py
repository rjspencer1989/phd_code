from process_config import notification_registration_client
from base_doc import BaseDoc

class Notifications(BaseDoc):
    def undo(self):
        rev_list = self.get_rev_list()
        result = ''
        if len(rev_list) == 0:
            result = self.undo_new()
        elif self.doc['hidden'] == True:
            result = self.undo_delete()
        else:
            result = self.undo_edit()
        return result

    def undo_new(self):
        notification_registration_client.delete(self.doc)
        updated = self.db.get(self.doc['_id'])
        return updated['_rev']

    def undo_delete(self):
        del self.doc['hidden']
        self.doc['status'] = 'done'
        self.db.save_doc(self.doc, force_update=True)
        notification_registration_client.register(self.doc)
        updated = self.db.get(self.doc['_id'])
        return updated['_rev']
