class ConnectionState(object):
    def __init__(self):
        self._id = "connection_state"
        self.collection = "connection_state"
        self.state = "connected"

    def get_doc(self):
        doc = {
            "_id" : self._id,
            "collection": self.collection,
            "state": self.state
        }
        return doc

    def set_field(self, field, value):
        setattr(self, field, value)
