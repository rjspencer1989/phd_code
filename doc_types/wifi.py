class Wifi(object):
    def __init__(self, ssid, password, mode, channel):
        self.ssid = ssid
        self.password = password
        self.mode = mode
        self.channel = channel
        self.status = 'pending'
        self.collection = 'wifi'
        self.encryption_type = 'wpa'