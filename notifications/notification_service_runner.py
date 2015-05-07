#!/usr/bin/python

from couchdbkit import *
from Queue import Queue
import threading
import ConfigParser
import os
from os.path import expanduser

config = ConfigParser.ConfigParser()
path = "%s/couchdb.conf" % (expanduser('~'))
config.read(path)
user = config.get('DEFAULT', 'ADMIN')
password = config.get('DEFAULT', 'ADMIN_PASSWORD')
port = config.get('DEFAULT', 'PORT')
remote_db = config.get('DEFAULT', 'DB')
server_name = config.get('DEFAULT', 'SERVER_NAME')

s = Server('http://%s:%s@%s:%s' % (user, password, server_name, port))
remoteDB = s[remote_db]
print remoteDB
remoteDbInf = remoteDB.info()


class NotificationRequestListener(threading.Thread):
    def __init__(self, threadName, queue):
        super(NotificationRequestListener, self).__init__(name=threadName)
        print "starting listener"
        self.sharedObject = queue

    def run(self):
        print 'listener running'
        remoteStream = ChangesStream(remoteDB, feed="continuous", heartbeat=True, since=remoteDbInf['update_seq'], filter='homework-remote/notification_request')
        for change in remoteStream:
            print change
            self.sharedObject.put(change)


class NotificationRequestProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        super(NotificationRequestProcessor, self).__init__(name=threadName)
        self.sharedObject = queue

    def sendNotification(self, notificationId, name, service, rows, message):
        success = False
        if len(rows) > 0:
            for row in rows:
                print row
                userDetails = row['value']
                encoded = service.encode('utf8')
                mod = __import__('NotificationServices', fromlist=[encoded])
                serviceClass = getattr(mod, service)
                result = serviceClass.sendNotification(notificationId, userDetails, message)
                success = result
        return success

    def run(self):
        while True:
            print "running"
            change = self.sharedObject.get()
            theId = change['id']
            print theId
            theRev = change['changes'][0]['rev']
            currentDoc = remoteDB.open_doc(theId, rev=theRev)
            if currentDoc['to'].lower() == 'everyone':
                res = remoteDB.view('homework-remote/notification_names', group=True)
                resList = res.all()
                if len(resList) > 0:
                    for nameItem in resList:
                        name = nameItem['key']
                        service = currentDoc['service'].lower()
                        key = [name, service]
                        serviceRes = remoteDB.view('homework-remote/notification_with_service', key=key)
                        serviceResAll = serviceRes.all()
                        if len(serviceResAll) > 0:
                            ret = self.sendNotification(currentDoc['id'], name, service, serviceResAll, currentDoc['body'])
                            if ret:
                                currentDoc['status'] = "done"
                            else:
                                currentDoc['status'] = "error"
            else:
                name = currentDoc['to']
                service = currentDoc['service'].lower()
                key = [name, service]
                serviceRes = remoteDB.view('homework-remote/notification_with_service', key=key)
                serviceResAll = serviceRes.all()
                if len(serviceResAll) > 0:
                    ret = self.sendNotification(theId, name, service, serviceResAll, currentDoc['body'])
                    if ret:
                        currentDoc['status'] = "done"
                    else:
                        currentDoc['status'] = "error"
            remoteDB.save_doc(currentDoc)

            self.sharedObject.task_done()

notificationQueue = Queue()
print notificationQueue
notificationProducer = NotificationRequestListener('prod', notificationQueue)
notificationConsumer = NotificationRequestProcessor('con', notificationQueue)
notificationProducer.start()
notificationConsumer.start()
