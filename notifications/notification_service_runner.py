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

    def get_registered_names(self):
        res = db.view('homework-remote/notification_names', group=True)
        res_all = res.all()
        name_list = []
        for row in res_all:
            name_list.append(row['key'])
        return name_list

    def run(self):
        while True:
            change = self.sharedObject.get()
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            current_doc = db.open_doc(the_id, rev=the_rev)
            name_list = []
            if current_doc['to'].lower() == 'everyone':
                name_list = self.get_registered_names()
            else:
                name_list = [current_doc['to']]
            if len(name_list) > 0:
                for name in name_list:
                    service = current_doc['service'].lower()
                    key = [name, service]
                    serviceRes = db.view('homework-remote/notification_with_service', key=key)
                    serviceResAll = serviceRes.all()
                    if len(serviceResAll) > 0:
                        ret = self.sendNotification(current_doc['id'], name, service, serviceResAll, current_doc['body'])
                        if ret:
                            current_doc['status'] = "done"
                        else:
                            current_doc['status'] = "error"
            else:
                current_doc['status'] = 'error'
            db.save_doc(current_doc)
            self.sharedObject.task_done()

notificationQueue = Queue()
notificationProducer = NotificationRequestListener('prod', notificationQueue)
notificationConsumer = NotificationRequestProcessor('con', notificationQueue)

if "ENV_TESTS" not in os.environ:
    notificationProducer.start()
    notificationConsumer.start()
