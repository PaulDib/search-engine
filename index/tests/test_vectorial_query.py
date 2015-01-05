import os
import unittest
from index.index import Index
from index.index_config import IndexConfig
from index.vectorial_query import VectorialQuery


class VectorialQueryTests(unittest.TestCase):

    def setUp(self):
        self._index = Index(
            os.path.dirname(os.path.realpath(__file__)) + "/test_data", IndexConfig())

    def test_VectorialQuery_simple(self):
        query = VectorialQuery("algebraic")
        results = query.execute(self._index)
        success = False
        for (doc_id, cos) in results:
            if doc_id == 1:
                success = True
        self.assertTrue(success)
