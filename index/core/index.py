'''
Main entry point of the package.
Provides the Index class that is able to index a collection
of documents and can be used to query them.
'''
import time
from multiprocessing import Pool
from functools import reduce
from .configuration import Configuration
from .constants import FILE, WORDS, START, END
from .document_index import DocumentIndex
from .utility import merge_dictionaries, tf_idf, tokenize


class Index:

    '''
    Class containing the whole index: documents and the lists of frequencies
    '''

    def __init__(self, data_files, stop_words_file="", stop_words=None):
        self._data_files = data_files
        if stop_words:
            self._stop_words = stop_words
        elif stop_words_file:
            self._read_stop_words(stop_words_file)
        else:
            self._stop_words = []
        self._index = dict()
        self._inverted_index = dict()
        self._number_of_docs = len(self._index)
        self._init_index()

    def search(self, word):
        '''Returns a list of doc_ids containing the requested word.'''
        standardized_word = tokenize(word)
        return self._inverted_index[standardized_word] \
            if standardized_word in self._inverted_index else []

    def document_by_id(self, doc_id):
        '''Returns a Document object for a requested doc id.'''
        return Configuration.DocumentParser().parse_document(
            self._get_document_content(doc_id)
        )

    def index_by_doc_id(self, doc_id):
        '''Returns a dictionary of words with their frequency in a document'''
        return self._index[doc_id] if doc_id in self._index else dict()

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
            self._index_files_threading(self._data_files, Configuration.number_of_threads)
        else:
            raise TypeError("dataFiles should be a string or a list")
        self._number_of_docs = len(self._index)

    def _index_files_threading(self, data_files, nbr_threads):
        start_time = time.time()
        if nbr_threads <= 1:
            indexes = [self._index_file(x) for x in data_files]
        else:
            with Pool(nbr_threads) as pool:
                indexes = pool.map(self._index_file, data_files)
        print("map ended in {0} seconds".format(time.time() - start_time))
        start_time = time.time()
        self._index = reduce(lambda x, y: merge_dictionaries(x, y, merge_dictionaries), indexes, dict())
        print("reduce ended in {0} seconds".format(time.time() - start_time))
        start_time = time.time()
        self._inverted_index = self._invert_index(self._index)
        print("inversion ended in {0} seconds".format(time.time() - start_time))

    def _invert_index(self, index):
        inverted_index = dict()
        for (doc_id, doc_index) in index.items():
            for word in doc_index[WORDS]:
                if not word in inverted_index:
                    inverted_index[word] = []
                inverted_index[word].append(doc_id)
        return inverted_index

    def _index_file(self, file_path):
        '''Populating the index with the results for one file.'''
        index = dict()
        parser = Configuration.DocumentParser(file_path)
        for (start_pos, end_pos, document) in parser.get_documents():
            self._save_document_location(document.get_doc_id(), file_path,
                                         start_pos, end_pos, index)
            self._add_document_to_index(document.get_doc_id(),
                                        document.get_content(), index)
        return index

    def _save_document_location(self, doc_id, file, start_pos, end_pos, index):
        '''Saves the position of the document in its file for later reads.'''
        index[doc_id] = [file, start_pos, end_pos, {}]

    def _add_document_to_index(self, doc_id, content, index):
        '''Populating the index with the result for one document.'''
        word_count = DocumentIndex(content, self._stop_words).get_word_count()
        index[doc_id][WORDS] = word_count

    def _get_document_content(self, doc_id):
        '''Outputs the document content as a list of lines'''
        if doc_id in self._index:
            content = ""
            doc_info = self._index[doc_id]
            with open(doc_info[FILE], encoding="utf8") as file_ptr:
                for i, line in enumerate(file_ptr):
                    if i >= doc_info[START] and i <= doc_info[END]:
                        content = content + "\n" + line
            return content
        raise ValueError("doc " + doc_id + " not found")
