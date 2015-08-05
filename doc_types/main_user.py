class MainUser(object):
    def __init__(self, name, service, timestamp=None):
        self._id = "main_user"
        self.collection = "main_user"
        self.name = name
        self.service = service,
        self.event_timestamp = timestamp

    def get_doc(self):
        doc = {
            "_id": self._id,
            "name": self.name,
            "service": self.service,
            "collection": self.collection,
            "event_timestamp": self.event_timestamp
        }
        return doc

    def set_field(self, field, value):
        setattr(self, field, value)
