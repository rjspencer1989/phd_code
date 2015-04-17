import RemoteNotify

def sendNotification(notificationId, to, body):
    nr = RemoteNotify.sendNotification("twitter", to, body)
    if nr is not None:
        if nr.code == 200:
            return RemoteNotify.getStatus(nr.notificationId)
