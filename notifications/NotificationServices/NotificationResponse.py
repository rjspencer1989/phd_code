class NotificationResponse(object):
    """Store the response from the app engine service"""
    def __init__(self, code, message, notificationId):
        super(NotificationResponse, self).__init__()
        self.code = code
        self.message = message
        self.notificationId = notificationId
