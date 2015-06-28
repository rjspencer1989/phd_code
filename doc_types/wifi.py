class Wifi(object):
    def __init__(self, ssid, password, mode):
        self.ssid = ssid
        self.password = password
        self.mode = mode
        self.status = 'pending'
        self.collection = 'wifi'