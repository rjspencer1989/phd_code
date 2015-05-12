#!/usr/bin/python
import os
import urllib
import urllib2
import cookielib
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('appengine.conf')
routerName = config.get('app data', 'ROUTER_NAME', 0)[1:-1]
targetAuthURL = 'https://2-dot-homework-notify.appspot.com/notify/2/'
request = urllib2.Request(targetAuthURL)
response = urllib2.urlopen(request)
responseBody = response.read()
if response.getcode() == 200:
    directory = os.path.dirname("/etc/homework/")
    if not os.path.exists(directory):
        os.makedirs(directory)
    f = open('/etc/homework/notification.conf', 'w')
    f.write("%s" % (responseBody))
    f.close()
    addURL = "https://2-dot-homework-notify.appspot.com/notify/2/%s/add/" % (responseBody)
    addRequestData = urllib.urlencode({"name": routerName})
    addRequest = urllib2.Request(addURL, data=addRequestData)
    addResponse = urllib2.urlopen(addRequest)
    addResponseBody = addResponse.read()
