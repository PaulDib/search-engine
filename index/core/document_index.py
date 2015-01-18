'''
Provides classes to index single documents.
'''
from .utility import get_word_list, count_tokens


class DocumentIndex(object):

    '''
    Class containing the indexing result for one document.
    The indexing will filter out stop words.
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
