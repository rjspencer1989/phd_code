#!/usr/bin/python

from couchdbkit import *
from Queue import Queue
import threading
import HomeworkConfigModifier
import ConnectedDevices
import ChangeNotification
import couchdbconfig
import NotificationRegistrationClient
from datetime import datetime
user = couchdbconfig.ADMIN_NAME
password = couchdbconfig.ADMIN_PASSWORD
port = couchdbconfig.SERVER_PORT
remoteDb = couchdbconfig.REMOTE_DB
s = Server('http://%s:%s@localhost:%d' % (user, password, port))
remoteDB = s[remoteDb]
remoteDbInf = remoteDB.info()


class RemoteChangeListener (threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.sharedObject = queue

    def run(self):
        remoteStream = ChangesStream(remoteDB, feed="continuous", heartbeat=True, since=remoteDbInf['update_seq'])
        for change in remoteStream:
            self.sharedObject.put(change)


class RemoteChangeProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.sharedObject = queue

    def run(self):
        while True:
            change = self.sharedObject.get()
            theId = change['id']
            theRev = change['changes'][0]['rev']
            print theId
            currentDoc = remoteDB.open_doc(theId, rev=theRev)
            status = HomeworkConfigModifier.updateConfig(currentDoc, remoteDB)
            if status == 'done':
                devices = ConnectedDevices.getConnectedDevices()
                if devices != 1:
                    for device in devices:
                        res = remoteDB.view('homework-remote/device_notification_service_mapping', key=device.getMac(), reduce=False)
                        resList = res.all()
				        if len(resList) == 1:
                            name = resList[0]['value']['name']
                            service = resList[0]['value']['service']
                            timestr = datetime.now().strftime("%H:%M:%S")
                            ChangeNotification.sendNotification(name, service, "network settings updated at %s" % (timestr))
            currentDoc['status'] = status
            print currentDoc['status']
            remoteDB.save_doc(currentDoc)
            self.sharedObject.task_done()

remoteQueue = Queue()
remoteProducer = RemoteChangeListener("remote producer", remoteQueue)
remoteConsumer = RemoteChangeProcessor("remote consumer", remoteQueue)
remoteProducer.start()
remoteConsumer.start()
