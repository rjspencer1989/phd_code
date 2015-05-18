import unittest
from process_config import CouchdbConfigParser, Undo, History


class TestProcessUndo(unittest.TestCase):
    def test_process_undo(self):
        undo_consumer = Undo.consumer
        event = {}
        doc = undo_consumer.get_doc_to_undo(event)
        rev_list = undo_consumer.get_rev_list(doc)
        result = undo_consumer.undo(rev_list)
