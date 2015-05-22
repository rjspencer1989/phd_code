import json
import os
import urllib
import urllib2

import notification_response


def getRouterID():
    return os.environ['APP_ENGINE_ROUTER_ID']


def sendNotification(service, to, body):
    data = {"to": to, "body": body}
    data = urllib.urlencode(data)

    router_id = getRouterID()
    if router_id is not None:
        url = "https://2-dot-homework-notify.appspot.com/notify/2/%s/%s" % (router_id, service.lower())
        content = ''
        req = urllib2.Request(url, data)
        try:
            response = urllib2.urlopen(req)
            content = response.readline()
            return notification_response.NotificationResponse(response.getcode(), "success", content)
        except urllib2.HTTPError, e:
            print e.reason
            return False

    return False


def getStatus(notificationId):
    router_id = getRouterID()
    if router_id is not None:
        data = {"notification": notificationId}
        data = urllib.urlencode(data)
        url = "https://2-dot-homework-notify.appspot.com/notify/2/%s/status" % (router_id)
        req = urllib2.Request(url, data)
        try:
            response = urllib2.urlopen(req)
            if response.code == 200:
                lines = response.readlines()
                if len(lines) > 0:
                    content = ''.join(lines)
                    jsonContent = json.loads(content)
                    if jsonContent['code'] == 200:
                        return True
                    return False
        except urllib2.HTTPError, e:
            print e.reason
            return False
    return False
