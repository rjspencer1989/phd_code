from process_config import couchdb_config_parser
from couchdbkit import *
from Queue import Queue
import threading
from process_config import reset

db = couchdb_config_parser.get_db()
db_info = db.info()


class ResetListener(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue
        self.since = db_info['update_seq']

    def run(self):
        changeStream = ChangesStream(db, feed="continuous", heartbeat=True, since=self.since, filter="homework-remote/reset")
        for change in changeStream:
            self.shared_object.put(change)


class ResetProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue
        self.devices = None

    def run(self):
        while(True):
            change = self.shared_object.get()
            reset.reset()
            self.shared_object.task_done()

changeQueue = Queue()
producer = ResetListener("producer", changeQueue)
consumer = ResetProcessor("consumer", changeQueue)
if 'ENV_TESTS' not in os.environ:
    producer.start()
    consumer.start()
