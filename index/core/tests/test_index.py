import unittest
import os
from ..index import Index
from ..index_config import IndexConfig
from ..utility import tf_idf
from ..constants import FILE, DOC_ID, COUNT, NORM_COUNT, WORDS, TFIDF, NORM_TFIDF, START, END


class IndexTests(unittest.TestCase):

    def test_inverted_index(self):
        '''
        Test the counts in the inverted index.
        Does not test the weights.
        '''
        index = Index(
            os.path.dirname(os.path.realpath(__file__)) + "/test_data", IndexConfig())
        expected = {
            'subtractions': {2:1},
            'language': {1:1, 2:1},
            'extraction': {2:1},
            'of': {2:1},
            'computers': {2:1},
            'for': {2:1},
            'algebraic': {1:1},
            'repeated': {2:1},
            'digital': {2:1},
            'preliminary': {1:2},
            'report': {1:1},
            'international': {1:1},
            'by': {2:1},
            'roots': {2:1}
        }
        self.assertEqual(expected, index._inverted_index)

    def test_inverted_index_withstop_words(self):
        '''
        Test the counts in the inverted index with stop words.
        Does not test the weights.
        '''
        config = IndexConfig()
        config.stop_words = ['of', 'by', 'for']
        index = Index(
            os.path.dirname(os.path.realpath(__file__)) + "/test_data", config)
        expected = {
            'subtractions': {2:1},
            'language': {1:1, 2:1},
            'extraction': {2:1},
            'computers': {2:1},
            'algebraic': {1:1},
            'repeated': {2:1},
            'digital': {2:1},
            'preliminary': {1:2},
            'report': {1:1},
            'international': {1:1},
            'roots': {2:1}
        }
        self.assertEqual(expected, index._inverted_index)

    def test_Search(self):
        expected = {1:1, 2:1}
        index = Index(
            os.path.dirname(os.path.realpath(__file__)) + "/test_data", IndexConfig())
        self.assertEqual([], index.search('thereShouldBeNoDocument'))
        self.assertEqual(expected, index.search('Language'))

    def test_index_by_doc_id(self):
        data_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_data")
        index = Index(data_path, IndexConfig())
        expected = {
            END: 44,
            FILE: data_path,
            START: 0,
            WORDS: {
                'algebraic': 1,
                'international': 1,
                'language': 1,
                'preliminary': 2,
                'report': 1
            }
        }
        self.assertEqual({}, index.index_by_doc_id(404))
        self.assertEqual(expected, index.index_by_doc_id(1))
