import CouchdbConfigParser
from couchdbkit import *
from Queue import Queue
import threading
import os
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

    def get_doc_to_undo(self, event):
        undo_id = event['doc_id']
        undo_doc = db.get(undo_id, revs_info=True)
        return undo_doc

    def get_rev_list(self, doc, undo_rev):
        revs_info = doc['_revs_info']
        rev_list = []
        for item in revs_info:
            rev_list.append(str(item['rev']))
        current_index = rev_list.index(undo_rev)
        print rev_list
        print current_index
        revs_list = rev_list[current_index + 1:]
        return revs_list

    def undo(self, doc, rev_list):
        undone_rev = ''
        if len(rev_list) == 0:
            if len(rev_list) == 1:
                res = db.delete_doc(undo_doc)
                undone_rev = res['rev']
            else:
                undoable_rev = ''
                for rev in rev_list:
                    cur = db.get(doc['id'], rev=rev)
                    if cur['collection'] == 'devices':
                        if cur['action'] == '':
                            undoable_rev = rev
                            break
                        else:
                            continue
                    else:
                        if cur['status'] == 'done':
                            undoable_rev = rev
                            break
                        else:
                            continue
                if undoable_rev != '':
                    cur = db.get(doc['id'], rev=undoable_rev)
                    res = db.save_doc(cur, force_update=True)
                    undone_rev = res['rev']
        return undone_rev

    def run(self):
        while(True):
            change = self.shared_object.get()
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            current_doc = db.open_doc(the_id, rev=the_rev)
            undo_doc = self.get_doc_to_undo(current_doc)
            rev_list = self.get_rev_list(undo_doc, current_doc['doc_rev'])
            undone_rev = self.undo(undo_doc, rev_list)
            if undone_rev != '':
                current_doc['process_undo'] = False
                db.save_doc(current_doc)
                History.addHistoryItem("Undo Configuration change", "Undo of %s" % (current_doc['description']), current_doc['user'], undo_id, undone_rev, True)
            self.shared_object.task_done()

changeQueue = Queue()
producer = UndoListener("producer", changeQueue)
consumer = UndoProcessor("consumer", changeQueue)
if "ENV_TESTS" not in os.environ:
    producer.start()
    consumer.start()
