class Devices(object):
    def __init__(self, mac_address, ip_address, device_name, user, lease_action, device_type, action):
        self._id = mac_address
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.device_name = device_name
        self.name = user,
        self.lease_action = lease_action
        self.device_type = device_type
        self.action = action
        self.state = 'pending'