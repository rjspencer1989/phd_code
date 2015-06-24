#!/usr/bin/python
import urllib2
import add_history

status = False
request = urllib2.Request('https://2-dot-homework-notify.appspot.com/notify/2/')
try:
    response = urllib2.urlopen(request)
    status = True
except urllib2.URLError as e:
    print e.reason
    status = False
    add_history.add_history_item('Internet connection error', str(e.reason), '', '', False)
