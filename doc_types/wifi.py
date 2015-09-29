class Wifi(object):
    def __init__(self, ssid, password, mode, channel, timestamp=None):
        self.ssid = ssid
        self.password = password
        self.mode = mode
        self.channel = channel
        self.status = 'pending'
        self.collection = 'wifi'
        self.encryption_type = 'wpa'
        self.with_bss = False
        self.event_timestamp = timestamp
        self._id = 'wifi'

    def get_doc(self):
        doc = {
            "_id": self._id,
            "ssid": self.ssid,
            "password": self.password,
            "mode": self.mode,
            "channel": self.channel,
            "status": self.status,
            "encryption_type": self.encryption_type,
            "collection": self.collection,
            "with_bss": self.with_bss,
            "event_timestamp": self.event_timestamp
        }
        
        if hasattr(self, '_rev'):
            doc["_rev"] = self._rev
        return doc

    def set_field(self, field, value):
        setattr(self, field, value)
