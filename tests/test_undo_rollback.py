import unittest
from process_config import couchdb_config_parser
from process_config.add_history import add_history_item
from undo import perform_undo
from undo.doc_types import request_revert
import time
import pprint
import datetime


class TestUndoRollback(unittest.TestCase):
    def test_rev_list_is_empty(self):
        self.assertTrue(False)
