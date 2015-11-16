class DNS(object):
    def __init__(self):
        self._id = "dns"
        self.collection = "dns"
        self.status = "active"

    def get_doc(self):
        return self.__dict__

    def set_field(self, field, value):
        setattr(field, value)
