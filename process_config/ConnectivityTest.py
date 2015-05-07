import urllib2
import History

status = False
request = urllib2.Request('https://2-dot-homework-notify.appspot.com/notify/2/')
try:
    response = urllib2.urlopen(request)
    status = True
except urllib2.URLError as e:
    print e.reason
    status = False
    History.addHistoryItem('Internet connection error', e.reason, 'Router', '', '', False)
