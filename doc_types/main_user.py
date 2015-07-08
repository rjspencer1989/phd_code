class MainUser(object):
    def __init__(self, name, service):
        self._id = "main_user"
        self.collection = "main_user"
        self.name = name
        self.service = service

    def get_doc(self):
        doc = {
            "_id": self._id,
            "name": self.name,
            "service": self.service,
            "collection": self.collection
        }
        return doc
