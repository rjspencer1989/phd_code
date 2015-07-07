class Notifications(object):
    def __init__(self, name, service, user):
        self.name = name
        self.service = service
        self.user = user
        self.collection = notifications
        self.status = done
