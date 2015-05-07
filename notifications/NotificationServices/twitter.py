import remote_notify


def sendNotification(notificationId, to, body):
    nr = remote_notify.sendNotification("twitter", to, body)
    if nr is not None:
        if nr.code == 200:
            return remote_notify.getStatus(nr.notificationId)
