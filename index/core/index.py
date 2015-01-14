'''
Main entry point of the package.
Provides the Index class that is able to index a collection
of documents and can be used to query them.
'''
from .document_index import DocumentIndex
from .document_parser import CACMDocumentParser
from .utility import merge_dictionaries, tf_idf, tokenize
from .constants import FILE, WORDS, START, END
from multiprocessing import Pool
from functools import reduce
import time

class Index:

    '''
    Class containing the whole index: documents and the lists of frequencies
    '''

    def __init__(self, data_files, stop_words_file="", stop_words=None,
                 parser_type=None):
        self._data_files = data_files
        if stop_words:
            self._stop_words = stop_words
        elif stop_words_file:
            self._read_stop_words(stop_words_file)
        else:
            self._stop_words = []
        if parser_type:
            self._parser_type = parser_type
        else:
            self._parser_type = CACMDocumentParser
        self._index = {}
        self._inverted_index = {}
        self._document_frequencies = {}
        self._count = 0
        self._number_of_docs = len(self._index)
        self._init_index()

    def search(self, word):
        '''Returns a list of doc_ids containing the requested word.'''
        standardized_word = tokenize(word)
        return self._inverted_index[standardized_word] \
            if standardized_word in self._inverted_index else {}

    def document_by_id(self, doc_id):
        '''Returns a Document object for a requested doc id.'''
        return self._parser_type().parse_document(
            self._get_document_content(doc_id)
        )

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

    def _read_stop_words(self, stop_word_file):
        '''
        Read a file containing stop words and populates the stop word list.'''
        if not stop_word_file:
            self._stop_words = []
        with open(stop_word_file) as file_ptr:
            self._stop_words = [x for x in file_ptr.read().splitlines()]

    def _init_index(self):
        '''Initializes the index and inverted index.'''
        if isinstance(self._data_files, str):
            self._index_files_threading([self._data_files], 1)
        elif type(self._data_files) is list:
            self._index_files_threading(self._data_files, 8)
        else:
            raise TypeError("dataFiles should be a string or a list")
        self._number_of_docs = len(self._index)

    def _index_files_threading(self, data_files, nbr_threads):
        start_time = time.time()
        if nbr_threads <= 1:
            indexes = map(self._index_file, data_files)
        else:
            with Pool(nbr_threads) as pool:x
                indexes = pool.map(self._index_file, data_files)
        print("map ended in {0} seconds".format(time.time() - start_time))
        start_time = time.time()
        self._index = reduce(lambda x, y: merge_dictionaries(x, y, merge_dictionaries), indexes, {})
        print("reduce ended in {0} seconds".format(time.time() - start_time))
        self._inverted_index = {}
        start_time = time.time()
        for (doc_id, doc_index) in self._index.items():
            for (word, word_count) in doc_index[WORDS].items():
                if not word in self._inverted_index:
                    self._inverted_index[word] = {}
                self._inverted_index[word][doc_id] = word_count
        print("inversion ended in {0} seconds".format(time.time() - start_time))

    def _index_file(self, file_path):
        '''Populating the index with the results for one file.'''
        index = {}
        parser = self._parser_type(file_path)
        for (start_pos, end_pos, document) in parser.get_documents():
            self._save_document_location(document.get_doc_id(), file_path,
                                         start_pos, end_pos, index)
            self._add_document_to_index(document.get_doc_id(),
                                        document.get_content(), index)
        return index

    def _save_document_location(self, doc_id, file, start_pos, end_pos, index):
        '''Saves the position of the document in its file for later reads.'''
        index[doc_id] = {FILE: file, START: start_pos, END: end_pos}

    def _add_document_to_index(self, doc_id, content, index):
        '''Populating the index with the result for one document.'''
        word_count = DocumentIndex(content, self._stop_words).get_word_count()
        index[doc_id][WORDS] = word_count
        #
        # self._inverted_index = merge_dictionaries(
        #     self._inverted_index, inverted_words, merge_dictionaries)

    def _get_document_content(self, doc_id):
        '''Outputs the document content as a list of lines'''
        if doc_id in self._index:
            content = ""
            doc_info = self._index[doc_id]
            with open(doc_info[FILE]) as file_ptr:
                for i, line in enumerate(file_ptr):
                    if i >= doc_info[START] and i <= doc_info[END]:
                        content = content + "\n" + line
            return content
        raise ValueError("doc " + doc_id + " not found")
