import os
import unittest
from math import sqrt
from ..index import Index
from ..vectorial_query import VectorialQueryTfIdf, VectorialQueryNormCount, VectorialQueryProbabilistic


class VectorialQueryTests(unittest.TestCase):

    def setUp(self):
        self._index = Index(
            os.path.dirname(os.path.realpath(__file__)) + "/test_data")

    def test_vectorial_query_tfidf(self):
        '''Tests a vectorial query that uses tfidf as a weight.'''
        query = VectorialQueryTfIdf("algebraic")
        results = query.execute(self._index)
        success = False
        for (doc_id, cos) in results:
            if doc_id == 1:
                success = True
        self.assertTrue(success)

    def test_vectorial_query_norm_count(self):
        '''Tests a vectorial query that uses normalized count as a weight.'''
        query = VectorialQueryNormCount("algebraic")
        results = query.execute(self._index)
        success = False
        doc_norm = sqrt(1+4*0.5*0.5)
        for (doc_id, cos) in results:
            if doc_id == 1:
                self.assertEqual(0.5/doc_norm, cos)
                success = True
        self.assertTrue(success)

    def test_vectorial_query_proba(self):
        '''Tests a vectorial query that uses normalized count as a weight.'''
        query = VectorialQueryProbabilistic("algebraic")
        results = query.execute(self._index)
        success = False
        for (doc_id, cos) in results:
            if doc_id == 1:
                success = True
        self.assertTrue(success)
