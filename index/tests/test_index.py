import unittest
import os
from index.index import Index
from index.index_config import IndexConfig
from index.utility import tf_idf

class IndexTests(unittest.TestCase):
    def test_InvertedIndex(self):
        '''
        Test the counts in the inverted index.
        Does not test the weights.
        '''
        index = Index(os.path.dirname(os.path.realpath(__file__)) + "/test_data", IndexConfig())
        expected = {
         'subtractions': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'language': [
            {'count': 1, 'norm_count': 0.5, 'docId': 1, 'tfidf': tf_idf(1, 2, 2), 'norm_tfidf': 0.0},
            {'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 2, 2), 'norm_tfidf': 0.0}
         ],
         'extraction': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'of': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'computers': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'for': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'algebraic': [{'count': 1, 'norm_count': 0.5, 'docId': 1, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'repeated': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'digital': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'preliminary': [{'count': 2, 'norm_count': 1.0, 'docId': 1, 'tfidf': tf_idf(2, 1, 2), 'norm_tfidf': 1.0}],
         'report': [{'count': 1, 'norm_count': 0.5, 'docId': 1, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'international': [{'count': 1, 'norm_count': 0.5, 'docId': 1, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'by': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'roots': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}]
        }
        self.assertEqual(expected, index._invertedIndex)

    def test_InvertedIndex_withStopWords(self):
        '''
        Test the counts in the inverted index with stop words.
        Does not test the weights.
        '''
        config = IndexConfig()
        config.stopWords = ['of', 'by','for']
        index = Index(os.path.dirname(os.path.realpath(__file__)) + "/test_data", config)
        expected = {
         'subtractions': [{'count': 1, 'docId': 2, 'norm_count': 1.0, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'language': [
            {'count': 1, 'norm_count': 0.5, 'docId': 1, 'tfidf': tf_idf(1, 2, 2), 'norm_tfidf': 0.0},
            {'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 2, 2), 'norm_tfidf': 0.0}
         ],
         'extraction': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'computers': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'algebraic': [{'count': 1, 'norm_count': 0.5, 'docId': 1, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'repeated': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'digital': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'preliminary': [{'count': 2, 'norm_count': 1.0, 'docId': 1, 'tfidf': tf_idf(2, 1, 2), 'norm_tfidf': 1.0}],
         'report': [{'count': 1, 'norm_count': 0.5, 'docId': 1, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'international': [{'count': 1, 'norm_count': 0.5, 'docId': 1, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}],
         'roots': [{'count': 1, 'norm_count': 1.0, 'docId': 2, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}]
        }
        self.assertEqual(expected, index._invertedIndex)

    def test_Search(self):
        expected = [
            {'count': 1, 'docId': 1, 'norm_count': 0.5, 'tfidf': 0.0, 'norm_tfidf': 0},
            {'count': 1, 'docId': 2, 'norm_count': 1.0, 'tfidf': 0.0, 'norm_tfidf': 0}
        ]
        index = Index(os.path.dirname(os.path.realpath(__file__)) + "/test_data", IndexConfig())
        self.assertEqual([], index.search('thereShouldBeNoDocument'))
        self.assertEqual(expected, index.search('Language'))

    def test_IndexByDocId(self):
        data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data")
        index = Index(data_path, IndexConfig())
        expected =  {
            'end': 44,
            'file': data_path,
            'start': 0,
            'words': {
                'algebraic': {'count': 1, 'norm_count': 0.5, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0},
                'international': {'count': 1, 'norm_count': 0.5, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0},
                'language': {'count': 1, 'norm_count': 0.5,'tfidf': tf_idf(1, 2, 2), 'norm_tfidf': 0.0},
                'preliminary': {'count': 2, 'norm_count': 1.0, 'tfidf': tf_idf(2, 1, 2), 'norm_tfidf': 1.0},
                'report': {'count': 1, 'norm_count': 0.5, 'tfidf': tf_idf(1, 1, 2), 'norm_tfidf': 1.0}
            }
        }
        self.assertEqual({}, index.indexByDocId(404))
        self.assertEqual(expected, index.indexByDocId(1))
