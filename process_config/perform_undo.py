import couchdb_config_parser
from couchdbkit import *
from Queue import Queue
import threading
import os
import add_history
db = couchdb_config_parser.getDB()
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
        revs_list = rev_list[current_index + 1:]
        return revs_list

    def undo_device_change(self, doc, revision):
        revs = self.get_rev_list(doc, revision)
        valid = []
        for rev in revs:
            current = db.get(doc['_id'], rev=rev)
            if current['changed_by'] == 'user':
                valid.append(rev)
        if len(valid) > 0:
            version_to_revert_to = db.get(doc['_id'], rev=valid[0])
            latest = db.get(doc['_id'])
            if version_to_revert_to['action'] != '':
                latest['action'] = version_to_revert_to['action']
            latest['device_name'] = version_to_revert_to['device_name']
            latest['device_type'] = version_to_revert_to['device_type']
            latest['name'] = version_to_revert_to['name']
            latest['notification_service'] = version_to_revert_to['notification_service']
            latest['changed_by'] = 'user'
            res = db.save_doc(latest, force_update=True)
            return res['rev']

    def undo(self, doc, rev_list):
        undone_rev = ''
        if len(rev_list) == 0:  # new doc
            res = db.delete_doc(doc)
            undone_rev = res['rev']
        else:  # has multiple revisions
            rev_to_revert_to = ''
            for rev in rev_list:
                cur = db.get(doc['_id'], rev=rev)
                if cur['status'] == 'done':
                    rev_to_revert_to = rev
                    break
                else:
                    continue
            if rev_to_revert_to != '':
                cur = db.get(doc['_id'], rev=rev_to_revert_to)
                res = db.save_doc(cur, force_update=True)
                undone_rev = res['rev']
            else:
                res = db.delete_doc(doc)
                undone_rev = res['rev']
        return undone_rev

    def run(self):
        while(True):
            change = self.shared_object.get()
            the_id = change['id']
            the_rev = change['changes'][0]['rev']
            current_doc = db.open_doc(the_id, rev=the_rev)
            undo_doc = self.get_doc_to_undo(current_doc)
            undone_rev = ''
            if undo_doc['collection'] == 'devices':
                undone_rev = self.undo_device_change(undo_doc)
            else:
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
