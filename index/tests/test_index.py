import unittest
import os
from index.index import Index
from index.index_config import IndexConfig

class IndexTests(unittest.TestCase):
    def setUp(self):
        self.index = Index(os.path.dirname(os.path.realpath(__file__)) + "/test_data", IndexConfig())

    def test_Index(self):
        test = {}
