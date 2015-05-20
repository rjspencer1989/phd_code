#!/usr/bin/python

from couchdbkit import *
from Queue import Queue
import threading
from process_config import CouchdbConfigParser
import os

db = CouchdbConfigParser.getDB()
db_info = db.info()


class NotificationRequestListener(threading.Thread):
    def __init__(self, threadName, queue):
        super(NotificationRequestListener, self).__init__(name=threadName)
        self.sharedObject = queue

    def run(self):
        changeStream = ChangesStream(db, feed="continuous", heartbeat=True, since=db_info['update_seq'], filter='homework-remote/notification_request')
        for change in changeStream:
            self.sharedObject.put(change)


class NotificationRequestProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        super(NotificationRequestProcessor, self).__init__(name=threadName)
        self.sharedObject = queue

    def sendNotification(self, notificationId, name, service, rows, message):
        success = False
        if len(rows) > 0:
            for row in rows:
                userDetails = row['value']
                encoded = service.encode('utf8')
                mod = __import__('NotificationServices', fromlist=[encoded])
                serviceClass = getattr(mod, service)
                result = serviceClass.sendNotification(notificationId, userDetails, message)
                success = result
        return success

    def run(self):
        while True:
            change = self.sharedObject.get()
            theId = change['id']
            theRev = change['changes'][0]['rev']
            currentDoc = db.open_doc(theId, rev=theRev)
            if currentDoc['to'].lower() == 'everyone':
                res = db.view('homework-remote/notification_names', group=True)
                resList = res.all()
                if len(resList) > 0:
                    for nameItem in resList:
                        name = nameItem['key']
                        service = currentDoc['service'].lower()
                        key = [name, service]
                        serviceRes = db.view('homework-remote/notification_with_service', key=key)
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
                serviceRes = db.view('homework-remote/notification_with_service', key=key)
                serviceResAll = serviceRes.all()
                if len(serviceResAll) > 0:
                    ret = self.sendNotification(theId, name, service, serviceResAll, currentDoc['body'])
                    if ret:
                        currentDoc['status'] = "done"
                    else:
                        currentDoc['status'] = "error"
            db.save_doc(currentDoc)

            self.sharedObject.task_done()

notificationQueue = Queue()
notificationProducer = NotificationRequestListener('prod', notificationQueue)
notificationConsumer = NotificationRequestProcessor('con', notificationQueue)
if "ENV_TESTS" not in os.environ:
    notificationProducer.start()
    notificationConsumer.start()
