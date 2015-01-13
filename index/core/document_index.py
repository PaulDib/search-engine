'''
Provides classes to index single documents.
'''
from .utility import get_word_list, count_tokens
import re


class StructuredDocument(object):

    '''
    Class representing one structured document for read access.
    '''

    def __init__(self, doc_id, title, content):
        self._doc_id = doc_id
        self._title = title
        self._content = content

    def get_content(self):
        '''Returns the indexed content of the document.'''
        return self._content

    def get_title(self):
        '''Returns the field that was marked as title of the document.'''
        return self._title

    def get_doc_id(self):
        '''Returns the doc id of the document.'''
        return self._doc_id



class PlainDocument(object):

    '''
    Class representing a plain text (non structured) document for read access.
    '''

    def __init__(self, content):
        self._content = content

    def get_content(self):
        '''Returns the whole content of the document.'''
        return self._content


class DocumentIndex(object):

    '''
    Class containing the indexing result for one document.
    If provided with a indexConfig, the indexing will parse the document
    and filter stop words. Otherwise, indexing will be done on
    the whole content.
    '''

    def __init__(self, content, stop_words=None):
        self.word_count = {}
        self._maxword_count = -1
        if stop_words:
            self._stop_words = stop_words
        else:
            self._stop_words = []
        self._init_index(content)

    def get_word_count(self):
        '''Returns a dictionary with words and their counts.'''
        return self.word_count

    def _init_index(self, content):
        '''Indexes one document and populates word_count.'''
        self.word_count = self._compute_word_count(content)

    def _compute_word_count(self, content):
        '''Computes the word count for a string.'''
        return count_tokens(self._tokenize(content))

    def _tokenize(self, content):
        '''Returns an array of tokens (clean words) in a string.'''
        tokens = get_word_list(content, self._stop_words)
        return tokens
