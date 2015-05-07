import remote_notify


def sendNotification(notificationId, to, body):
    nr = remote_notify.sendNotification("email", to, body)
    if nr is not None and nr is not False:
        print "sending email to %s with content %s" % (to, body)
        print nr.code
        if nr.code == 200:
            return True
        return False
