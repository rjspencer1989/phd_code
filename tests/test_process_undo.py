import unittest
from process_config import CouchdbConfigParser, Undo, History


class TestProcessUndo(unittest.TestCase):
    def test_process_undo_new_doc(self):
        undo_consumer = Undo.consumer
        nd = {
            "collection": "notifications",
            "status": "done",
            "name": "Rob",
            "service": "twitter",
            "user": "rjspencer1989"
        }
        db = CouchdbConfigParser.getDB()
        res = db.save_doc(nd)
        res2 = db.save_doc(nd)
        event_res = History.add_history_item("new notification", "added notification mapping for Rob using Twitter and username rjspencer1989", "Rob", res2['id'], res2['rev'], True)
        event = db.get(event_res['id'])
        doc = undo_consumer.get_doc_to_undo(event)
        rev_list = undo_consumer.get_rev_list(doc, res2['rev'])
        print rev_list
        result = undo_consumer.undo(rev_list)
        db.delete_doc(res['id'])
        db.delete_doc(event_res['id'])
