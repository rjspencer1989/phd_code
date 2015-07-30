class Wifi(object):
    def __init__(self, ssid, password, mode, channel):
        self.ssid = ssid
        self.password = password
        self.mode = mode
        self.channel = channel
        self.status = 'pending'
        self.collection = 'wifi'
        self.encryption_type = 'wpa'

    def get_doc(self):
        doc = {
            "ssid": self.ssid,
            "password": self.password,
            "mode": self.mode,
            "channel": self.channel,
            "status": self.status,
            "encryption_type": self.encryption_type,
            "collection": self.collection
        }
        return doc

    def set_field(self, field, value):
        setattr(self, field, value)
