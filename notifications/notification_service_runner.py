#!/usr/bin/python

from couchdbkit import *
from Queue import Queue
import threading
from ..process_config import CouchdbConfigParser
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

    def send_notification(self, notification_id, name, service, user, message):
        encoded = service.encode('utf8')
        mod = __import__('NotificationServices', fromlist=[encoded])
        service_class = getattr(mod, service)
        result = service_class.sendNotification(notification_id, user_details, message)
        return result

    def get_user_names(self, name, service):
        if name.lower() == 'everyone':
            start_key = [service, ""]
            end_key = [service, {}]
        else:
            start_key = [service, name]
            end_key = [service, name]
        service_res = db.view('homework-remote/notification_with_service', startkey=start_key, endkey=end_key)
        service_res_all = serviceRes.all()
        if len(service_res_all) > 0:
            return service_res_all
        return None

    def process_notification(self, doc):
        usernames = self.get_user_names(doc['to'], doc['service'])
        ret = False
        if usernames is not None:
            for result in usernames:
                service = doc['service'].lower()
                name = doc['to']
                if name.lower() == 'everyone':
                    name = result['key'][1]
                user = result['value']
                ret = self.send_notification(doc['_id'], name, service, user, doc['body'])
            if ret:
                doc['status'] = "done"
            else:
                doc['status'] = "error"
        else:
            doc['status'] = 'error'
        db.save_doc(doc)

    def run(self):
        while True:
            change = self.sharedObject.get()
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            doc = db.open_doc(the_id, rev=the_rev)
            self.process_notification(doc)
            self.sharedObject.task_done()

notification_queue = Queue()
notification_producer = NotificationRequestListener('prod', notification_queue)
notification_consumer = NotificationRequestProcessor('con', notification_queue)

if "ENV_TESTS" not in os.environ:
    notification_producer.start()
    notification_consumer.start()
