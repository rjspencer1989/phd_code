import unittest
from process_config import CouchdbConfigParser, Undo, History


class TestProcessUndo(unittest.TestCase):
    def test_process_undo(self):
        undo_processor = Undo.UndoProcessor()
        event = {}
        doc = undo_processor.get_doc_to_undo(event)
        rev_list = undo_processor.get_rev_list(doc)
        result = undo_processor.undo(rev_list)
