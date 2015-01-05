'''
Represents a vectorial query using tf-idf.
'''
from .document_index import DocumentIndex


class VectorialQuery(object):

    '''Represents a vectorial query using tf-idf.'''

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
        result_dict = index.getMatchingDocuments(self._index)
        sorted_results = sorted(result_dict.items(),
                                key=lambda x: x[1],
                                reverse=True)
        return sorted_results
