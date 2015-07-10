import time


class Devices(object):
    def __init__(self, mac_address, ip_address, host_name, device_name, user, lease_action, device_type, state, notification_service, port):
        self._id = mac_address
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.device_name = device_name
        self.name = user
        self.lease_action = lease_action
        self.device_type = device_type
        self.action = ""
        self.state = state
        self.collection = "device"
        self.host_name = host_name
        self.notification_service = notification_service
        self.timestamp = time.time()
        self.port = port
        self.connection_event = "connect"
        self.changed_by = "system"
        
    def get_doc(self):
        doc = {
            "_id": self._id,
            "mac_address": self.mac_address,
            "ip_address": self.ip_address,
            "collection": self.collection,
            "action": self.action,
            "device_name": self.device_name,
            "name": self.name,
            "lease_action": self.lease_action,
            "host_name": self.host_name,
            "state": self.state,
            "device_type": self.device_type,
            "notification_service": self.notification_service,
            "timestamp": self.timestamp,
            "port": self.port,
            "connection_event": self.connection_event,
            "changed_by": self.changed_by
        }
        return doc

    def set_field(self, field, value):
        self[field] = value