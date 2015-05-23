import unittest
from process_config import couchdb_config_parser, perform_rollback
import time


class TestProcessRollback(unittest.TestCase):
    def test_process_rollback(self):
        timestamp = time.time() - 20
        result = perform_rollback.perform_rollback(timestamp)
        self.assertEqual(result, True)
