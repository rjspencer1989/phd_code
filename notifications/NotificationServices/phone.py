import json
import RemoteNotify
import urllib
import urllib2

def sendNotification(notificationId, to, body):
    nr = RemoteNotify.sendNotification("phone", to, body)
    if nr is not None and nr is not False:
        if nr.code == 200:
            return RemoteNotify.getStatus(nr.notificationId)
