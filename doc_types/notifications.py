class Notifications(object):
    def __init__(self, name, service, user):
        self.name = name
        self.service = service
        self.user = user
        self.collection = "notifications"
        self.status = "done"

    def get_doc(self):
        doc = {
            "name": self.name,
            "service": self.service,
            "user": self.user,
            "collection": self.collection,
            "status": self.status
        }
        return doc
