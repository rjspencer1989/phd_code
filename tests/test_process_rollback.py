import unittest
from process_config import couchdb_config_parser, rollback
import time


class TestProcessRollback(unittest.TestCase):
    @unittest.skip("need to create implementation classes")
    def test_process_rollback(self):
        timestamp = time.time() - 20
        result = Rollback.perform_rollback(timestamp)
        self.assertEqual(result, True)
