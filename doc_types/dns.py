class DNS(object):
    def __init__(self):
        self._id = "dns"
        self.collection = "dns"
        self.dns_status = "active"
        self.status = "done"

    def get_doc(self):
        return self.__dict__

    def set_field(self, field, value):
        setattr(self, field, value)
