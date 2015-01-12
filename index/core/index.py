'''
Main entry point of the package.
Provides the Index class that is able to index a collection
of documents and can be used to query them.
'''
from .document_index import DocumentIndex, CACMStructuredDocument
from .utility import merge_dictionaries, tf_idf, tokenize
from .constants import FILE, WORDS, START, END


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
        standardized_word = tokenize(word)
        return self._inverted_index[standardized_word] \
            if standardized_word in self._inverted_index else {}

    def document_by_id(self, doc_id):
        '''Returns a Document object for a requested doc id.'''
        return CACMStructuredDocument(self._get_document_content(doc_id),
                                  self._config)

    def index_by_doc_id(self, doc_id):
        '''Returns a dictionary of words with their frequency in a document'''
        return self._index[doc_id] if doc_id in self._index else {}

    def get_all_doc_ids(self):
        '''Returns a list with all doc ids in the index'''
        return [doc_id for doc_id in self._index]

    def compute_tfidf_for_word(self, word, vector):
        '''
        Computes the tfidf for one word in one vector,
        using the current index statistics.
        '''
        if word in self._inverted_index:
            tfidf = tf_idf(vector[word],
                           len(self._inverted_index[word]),
                           self._number_of_docs)
            return tfidf
        else:
            return 0.0

    def _init_index(self):
        '''Initializes the index and inverted index.'''
        if isinstance(self._data_files, str):
            self._index_file(self._data_files)
        elif type(self._data_files) is list:
            for file in self._data_files:
                self._index_file(file)
        else:
            raise TypeError("dataFiles should be a string or a list")
        self._number_of_docs = len(self._index)

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

    def _save_document_location(self, doc_id, file, start_pos, end_pos):
        '''Saves the position of the document in its file for later reads.'''
        self._index[doc_id] = {FILE: file, START: start_pos, END: end_pos}

    def _add_document_to_index(self, doc_id, content):
        '''Populating the index with the result for one document.'''
        word_count = DocumentIndex(content, self._config).get_word_count()
        self._index[doc_id][WORDS] = word_count
        inverted_words = {
            word: {doc_id: word_count[word]}
            for word in word_count if word_count[word] > 0
        }
        self._inverted_index = merge_dictionaries(
            self._inverted_index, inverted_words, merge_dictionaries)

    def _get_document_content(self, doc_id):
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
