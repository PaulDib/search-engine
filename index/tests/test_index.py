import unittest
import os
from index.index import Index
from index.index_config import IndexConfig

class IndexTests(unittest.TestCase):
    def test_Index(self):
        index = Index(os.path.dirname(os.path.realpath(__file__)) + "/test_data", IndexConfig())
        expected = {
         'subtractions': [2],
         'language': [1, 2],
         'extraction': [2],
         'of': [2],
         'computers': [2],
         'for': [2],
         'algebraic': [1],
         'repeated': [2],
         'digital': [2],
         'preliminary': [1],
         'report': [1],
         'international': [1],
         'by': [2],
         'roots': [2]
        }
        self.assertEqual(expected, index._invertedIndex)

    def test_Index_withStopWords(self):
        config = IndexConfig()
        config.stopWords = ['of', 'by','for']
        index = Index(os.path.dirname(os.path.realpath(__file__)) + "/test_data", config)
        expected = {
         'subtractions': [2],
         'language': [1, 2],
         'extraction': [2],
         'computers': [2],
         'algebraic': [1],
         'repeated': [2],
         'digital': [2],
         'preliminary': [1],
         'report': [1],
         'international': [1],
         'roots': [2]
        }
        self.assertEqual(expected, index._invertedIndex)
