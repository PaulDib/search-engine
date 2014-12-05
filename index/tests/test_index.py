import unittest
import os
from index.index import Index
from index.index_config import IndexConfig

class IndexTests(unittest.TestCase):
    def test_Index(self):
        index = Index(os.path.dirname(os.path.realpath(__file__)) + "/test_data", IndexConfig())
        expected = {
         'subtractions': [{'count': 1, 'docId': 2}],
         'language': [{'count': 1, 'docId': 1}, {'count': 1, 'docId': 2}],
         'extraction': [{'count': 1, 'docId': 2}],
         'of': [{'count': 1, 'docId': 2}],
         'computers': [{'count': 1, 'docId': 2}],
         'for': [{'count': 1, 'docId': 2}],
         'algebraic': [{'count': 1, 'docId': 1}],
         'repeated': [{'count': 1, 'docId': 2}],
         'digital': [{'count': 1, 'docId': 2}],
         'preliminary': [{'count': 2, 'docId': 1}],
         'report': [{'count': 1, 'docId': 1}],
         'international': [{'count': 1, 'docId': 1}],
         'by': [{'count': 1, 'docId': 2}],
         'roots': [{'count': 1, 'docId': 2}]
        }
        self.assertEqual(expected, index._invertedIndex)

    def test_Index_withStopWords(self):
        config = IndexConfig()
        config.stopWords = ['of', 'by','for']
        index = Index(os.path.dirname(os.path.realpath(__file__)) + "/test_data", config)
        expected = {
         'subtractions': [{'count': 1, 'docId': 2}],
         'language': [{'count': 1, 'docId': 1}, {'count': 1, 'docId': 2}],
         'extraction': [{'count': 1, 'docId': 2}],
         'computers': [{'count': 1, 'docId': 2}],
         'algebraic': [{'count': 1, 'docId': 1}],
         'repeated': [{'count': 1, 'docId': 2}],
         'digital': [{'count': 1, 'docId': 2}],
         'preliminary': [{'count': 2, 'docId': 1}],
         'report': [{'count': 1, 'docId': 1}],
         'international': [{'count': 1, 'docId': 1}],
         'roots': [{'count': 1, 'docId': 2}]
        }
        self.assertEqual(expected, index._invertedIndex)
