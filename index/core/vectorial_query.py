'''
Represents a vectorial query using tf-idf.
'''
from .constants import NORM_COUNT
from .document_index import DocumentIndex


def _sort_results(result_dict):
    '''Sort results by descending weight.'''
    return sorted(result_dict.items(), key=lambda x: x[1], reverse=True)


class VectorialQuery(object):

    '''Represents an abstract vectorial query.'''

    def __init__(self, query):
        self._query = query
        self._init_index()

    def _init_index(self):
        '''Initializes the index-like structure for the query.'''
        doc_idx = DocumentIndex(self._query)
        self._index = doc_idx.get_word_count()

    def execute(self, index):
        '''
        Executes the query against the index
        and returns documents sorted by descending matching score.
        '''
        pass


class VectorialQueryTfIdf(VectorialQuery):

    '''Represents a vectorial query using tf-idf.'''

    def execute(self, index):
        '''
        Executes the query against the index
        and returns documents sorted by descending matching score.
        '''
        result_dict = index.get_matching_documents(self._index)
        return _sort_results(result_dict)


class VectorialQueryNormCount(VectorialQuery):

    '''Represents a vectorial query using normalized count.'''

    def execute(self, index):
        '''
        Executes the query against the index
        and returns documents sorted by descending matching score.
        '''
        result_dict = index.get_matching_documents(self._index, NORM_COUNT)
        return _sort_results(result_dict)
