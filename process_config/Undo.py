import CouchdbConfigParser
from couchdbkit import *
from Queue import Queue
import threading
import History
db = CouchdbConfigParser.getDB()
db_info = db.info()


class UndoListener(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        changeStream = ChangesStream(db, feed="continuous", heartbeat=True, since=db_info['update_seq'], filter="homework-remote/undo")
        for change in changeStream:
            self.shared_object.put(change)


class UndoProcessor(threading.Thread):
    def __init__(self, threadName, queue):
        threading.Thread.__init__(self, name=threadName)
        self.shared_object = queue

    def run(self):
        while(True):
            change = self.shared_object.get()
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            current_doc = db.open_doc(the_id, rev=the_rev)
            undo_id = current_doc['doc_id']
            undo_rev = current_doc['doc_rev']
            undo_doc = db.get(undo_id, revs_info=True)
            revs_info = undo_doc['_revs_info']
            revs_list = []
            for item in revs:
                rev_list.append(str(item['rev']))
            current_index = rev_list.index(undo_rev)
            undo_rev = 0
            undone_rev = ''
            if len(rev_list) == 1:
                undo_doc['_deleted'] = True
                res = db.save_doc(undo_doc)
                undone_rev = res['rev']
            elif current_index < len(rev_list) - 1:
                undo_rev = rev_list[current_index + 1]
                prev_doc = db.get(undo_id, rev=undo_rev)
                res = db.save_doc(prev_doc, force_update=True)
                undone_rev = res['rev']
            current_doc['process_undo'] = False
            db.save_doc(current_doc)

            History.addHistoryItem("Undo Configuration change", "Undo of %s" % (current_doc['description']), current_doc['user'], undo_id, undone_rev, True)
            self.shared_object.task_done()
changeQueue = Queue()
producer = UndoListener("producer", changeQueue)
consumer = UndoProcessor("consumer", changeQueue)
producer.start()
consumer.start()
