from base_doc import BaseDoc


class Request_revert(BaseDoc):
    def undo(self):
        rev_list = self.get_rev_list()
