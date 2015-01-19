'''
Provides classes to execute vectorial and probabilistic queries.
'''
from .constants import WORDS
from .document_index import DocumentIndex
from .utility import norm, scalar_product, probabilistic_weight


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
        self._word_vector = doc_idx.get_word_count()

    def execute(self, index):
        '''
        Executes the query against the index
        and returns documents sorted by descending matching score.
        '''
        return self._execute(index, self._weighting_function)

    def _execute(self, index, weighting_function):
        '''
        Internal execution of the vectorial query that uses
        a custom weighting function.
        '''
        result_dict = {}
        query_vector = {
            word:weighting_function(word, self._word_vector, index)
            for word in self._word_vector
        }
        query_norm = norm(query_vector)
        for word in query_vector:
            documents = index.search(word)
            for doc_id in documents:
                result_dict[doc_id] = 0
        for doc_id in result_dict:
            document = index.index_by_doc_id(doc_id)[WORDS]
            doc_vector = {
                word:weighting_function(word, document, index)
                for word in document
            }
            doc_norm = norm(doc_vector)
            result_dict[doc_id] = \
                scalar_product(query_vector, doc_vector) / (query_norm*doc_norm)
        return _sort_results(result_dict)

    def _weighting_function(self, word, word_vector, index):
        pass


class VectorialQueryTfIdf(VectorialQuery):

    '''Represents a vectorial query using tf-idf.'''

    def _weighting_function(self, word, word_vector, index):
        return index.compute_tfidf_for_word(word, word_vector)


class VectorialQueryNormCount(VectorialQuery):

    '''Represents a vectorial query using normalized count.'''

    def _weighting_function(self, word, word_vector, index):
        max_freq = max(word_vector.values())
        return word_vector[word] / max_freq


class VectorialQueryProbabilistic(VectorialQuery):

    '''Represents a probabilistic query.'''

    def execute(self, index):
        '''
        Executes the query against the index
        and returns documents sorted by descending matching score.
        '''
        result_dict = {}
        number_of_docs = len(index.get_all_doc_ids())
        for word in self._word_vector:
            documents = index.search(word)
            doc_frequency = len(documents)
            for doc_id in documents:
                irrelevant_prob = doc_frequency / number_of_docs
                relevant_prob = 1/3 + 2/3*doc_frequency/number_of_docs
                term = probabilistic_weight(relevant_prob) \
                    - probabilistic_weight(irrelevant_prob)
                if doc_id in result_dict:
                    result_dict[doc_id] += term
                else:
                    result_dict[doc_id] = term
        return _sort_results(result_dict)
