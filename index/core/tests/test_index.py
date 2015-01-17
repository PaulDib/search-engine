import unittest
import os
from ..index import Index


class IndexTests(unittest.TestCase):

    def test_inverted_index(self):
        '''
        Test the counts in the inverted index.
        Does not test the weights.
        '''
        index = Index(os.path.dirname(os.path.realpath(__file__)) + "/test_data")
        expected = {
            'subtract': [2],
            'languag': [1, 2],
            'extract': [2],
            'of': [2],
            'comput': [2],
            'for': [2],
            'algebra': [1],
            'repeat': [2],
            'digit': [2],
            'preliminari': [1],
            'report': [1],
            'intern': [1],
            'by': [2],
            'root': [2]
        }
        self.assertEqual(expected, index._inverted_index)

    def test_inverted_index_withstop_words(self):
        '''
        Test the counts in the inverted index with stop words.
        Does not test the weights.
        '''
        index = Index(
            os.path.dirname(os.path.realpath(__file__)) + "/test_data",
            stop_words=['of', 'by', 'for'])
        expected = {
         'subtract': [2],
            'languag': [1,2],
            'extract': [2],
            'comput': [2],
            'algebra': [1],
            'repeat': [2],
            'digit': [2],
            'preliminari': [1],
            'report': [1],
            'intern': [1],
            'root': [2]
        }
        self.assertEqual(expected, index._inverted_index)

    def test_search(self):
        expected = [1, 2]
        index = Index(os.path.dirname(os.path.realpath(__file__)) + "/test_data")
        self.assertEqual({}, index.search('thereShouldBeNoDocument'))
        self.assertEqual(expected, index.search('Language'))

    def test_index_by_doc_id(self):
        data_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_data")
        index = Index(data_path)
        expected = [
            data_path,
            0,
            44,
            {
                'algebra': 1,
                'intern': 1,
                'languag': 1,
                'preliminari': 2,
                'report': 1
            }
        ]
        self.assertEqual({}, index.index_by_doc_id(404))
        self.assertEqual(expected, index.index_by_doc_id(1))
