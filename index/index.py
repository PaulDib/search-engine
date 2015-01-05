'''
Main entry point of the package.
Provides the Index class that is able to index a collection 
of documents and can be used to query them.
'''
from .document_index import DocumentIndex, StructuredDocument
from .utility import merge_dictionaries, tf_idf, norm
from .constants import FILE, DOC_ID, COUNT, NORM_COUNT, WORDS, TFIDF, NORM_TFIDF, START, END


class Index:

    '''
    Class containing the whole index: documents and the lists of frequencies
    '''

    def __init__(self, dataFiles, indexConfig):
        self._config = indexConfig
        self._data_files = dataFiles
        self._index = {}
        self._inverted_index = {}
        self._document_frequencies = {}
        self._number_of_docs = len(self._index)
        self._init_index()

    def search(self, word):
        '''Returns a list of doc_ids containing the requested word.'''
        standardized_word = word.lower()
        return self._inverted_index[standardized_word] if standardized_word in self._inverted_index else []

    def document_by_id(self, doc_id):
        '''Returns a Document object for a requested doc id.'''
        return StructuredDocument(self._getdocument_content(doc_id), self._config)

    def index_by_doc_id(self, doc_id):
        '''Returns a dictionary of words with their frequency in a document'''
        return self._index[doc_id] if doc_id in self._index else {}

    def get_matching_documents(self, document_words, weight_key=NORM_TFIDF):
        '''
        Returns documents similar to the input by computing the cosine of the
        input document to the collection, using a specific weight as components
        of the vectors.
        '''
        query_vector = self._compute_query_vector(
            document_words, self._compute_tfidf_for_word)
        results = self._scalar_product_with_index(query_vector, weight_key)
        results = self._normalize_results(query_vector, results, weight_key)
        return results

    def get_all_doc_ids(self):
        '''Returns a list with all doc ids in the index'''
        return [doc_id for doc_id in self._index]

    def _scalar_product_with_index(self, query_vector, weight_key):
        '''
        Computes the scalar product between a query vector and the indexed docs.
        '''
        results = {}
        for word in query_vector:
            if word in self._inverted_index:
                weight_input = query_vector[word]
                for doc in self._inverted_index[word]:
                    doc_id = doc[DOC_ID]
                    weight_doc = doc[weight_key]
                    if doc_id in results:
                        results[doc_id] = results[
                            doc_id] + weight_doc * weight_input
                    else:
                        results[doc_id] = weight_doc * weight_input
        return results

    def _normalize_results(self, query_vector, results, weight_key):
        '''
        Divide results by the norm of the two input vectors.
        '''
        query_norm = norm(query_vector)
        for doc_id in results:
            result_norm = norm(self._index[doc_id][WORDS], weight_key)
            results[doc_id] = results[doc_id] / (result_norm * query_norm)
        return results

    def _compute_query_vector(self, query_words, statistic_function):
        query_vector = {}
        for word in query_words:
            query_vector[word] = statistic_function(word, query_words)
        return query_vector

    def _compute_tfidf_for_word(self, word, vector):
        if word in self._document_frequencies:
            weight_input = tf_idf(vector[word][COUNT],
                                  self._document_frequencies[word],
                                  self._number_of_docs)
            return weight_input
        else:
            return 0.0

    def _compute_norm_count_for_word(self, word, vector):
        return vector[word][NORM_COUNT]

    def _init_index(self):
        if isinstance(self._data_files, str):
            self._index_file(self._data_files)
        elif type(self._data_files) is list:
            for file in self._data_files:
                self._index_file(file)
        else:
            raise TypeError("dataFiles should be a string or a list")

        self._init_statistics()

    def _index_file(self, file):
        '''Populating the index with the results for one file.'''
        with open(file) as file_ptr:
            doc_id = None
            document_content = []
            i = 0
            document_start_pos = 0
            for i, line in enumerate(file_ptr):
                if line.startswith(self._config.id_marker):
                    if doc_id is not None:
                        # Indexing previous document
                        self._save_document_location(
                            doc_id, file, document_start_pos, i - 1)
                        self._add_document_to_index(doc_id, document_content)
                    doc_id = int(line[len(self._config.id_marker):])
                    document_start_pos = i
                    document_content = []
                document_content = document_content + [line]

            # Handling last document.
            if doc_id is not None:
                self._save_document_location(
                    doc_id, file, document_start_pos, i - 1)
                self._add_document_to_index(doc_id, document_content)

    def _init_statistics(self):
        # TODO: Refactor
        self._document_frequencies = {}
        self._number_of_docs = len(self._index)
        for word in self._inverted_index:
            doc_frequency = len(self._inverted_index[word])
            self._document_frequencies[word] = doc_frequency
            for doc in self._inverted_index[word]:
                tfidf = tf_idf(doc[COUNT], doc_frequency, self._number_of_docs)
                doc[TFIDF] = tfidf
                self._index[doc[DOC_ID]][WORDS][word][TFIDF] = tfidf
            max_tfidf = max({doc[TFIDF] for doc in self._inverted_index[word]})
            if max_tfidf > 0:
                for doc in self._inverted_index[word]:
                    doc[NORM_TFIDF] = doc[TFIDF] / max_tfidf
                    self._index[doc[DOC_ID]][WORDS][word][NORM_TFIDF] = \
                        doc[TFIDF] / max_tfidf
            else:
                for doc in self._inverted_index[word]:
                    doc[NORM_TFIDF] = doc[TFIDF]
                    self._index[doc[DOC_ID]][WORDS][
                        word][NORM_TFIDF] = doc[TFIDF]

    def _save_document_location(self, doc_id, file, start_pos, end_pos):
        '''Saves the position of the document in its file for later reads.'''
        self._index[doc_id] = {FILE: file, START: start_pos, END: end_pos}

    def _add_document_to_index(self, doc_id, content):
        '''Populating the index with the result for one document.'''
        word_count = DocumentIndex(content, self._config).get_word_count()
        self._index[doc_id][WORDS] = word_count
        inverted_words = {
            word: [{DOC_ID: doc_id, COUNT: word_count[word][COUNT], NORM_COUNT:  word_count[word][NORM_COUNT]}]
            for word in word_count if word_count[word][COUNT] > 0
        }
        self._inverted_index = merge_dictionaries(
            self._inverted_index, inverted_words)

    def _getdocument_content(self, doc_id):
        '''Outputs the document content as a list of lines'''
        if doc_id in self._index:
            content = []
            doc_info = self._index[doc_id]
            with open(doc_info[FILE]) as file_ptr:
                for i, line in enumerate(file_ptr):
                    if i >= doc_info[START] and i <= doc_info[END]:
                        content = content + [line]
            return content
        raise ValueError("doc " + doc_id + " not found")
