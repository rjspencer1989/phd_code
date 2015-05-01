import json
import remote_notify
import urllib
import urllib2

def sendNotification(notificationId, to, body):
    nr = remote_notify.sendNotification("phone", to, body)
    if nr is not None and nr is not False:
        if nr.code == 200:
            return remote_notify.getStatus(nr.notificationId)
