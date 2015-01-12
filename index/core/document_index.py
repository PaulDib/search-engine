'''
Provides classes to index single documents.
'''
from .utility import get_word_list, count_tokens, merge_dictionaries
import re


class CACMStructuredDocument(object):

    '''
    Class representing one structured document for read access.
    '''

    def __init__(self, content, index_config):
        self._config = index_config
        self._content = content
        self.field_positions = {}
        self._get_field_positions()

    def get_content(self):
        '''Returns the indexed content of the document.'''
        res = {}
        for field in self._config.focus_fields:
            res[field] = self._get_field_content(field)
        return res

    def get_title(self):
        '''Returns the field that was marked as title of the document.'''
        result = self._get_field_content(self._config.title_field).strip()
        result = re.sub(r'(\s)+', r' ', result)
        return result

    def _get_field_content(self, field):
        '''Returns the content of the specified field.'''
        start_pos = self.field_positions[field] + 1
        if start_pos <= 0:
            return ""
        next_fields = {v for (k, v) in self.field_positions.items()
                       if v > start_pos}
        stop_pos = min(next_fields) if next_fields else len(self._content)
        return "\n".join(self._content[start_pos:stop_pos])

    def _get_field_positions(self):
        '''
        Populates field_positions = { 'fieldName': start_position } dictionary.
        '''
        self.field_positions = {}
        for field in self._config.fields:
            self.field_positions[field] = \
                next((i for i, l in enumerate(self._content)
                      if l.startswith(field)), -1)


class PlainDocument(object):

    '''
    Class representing a plain text (non structured) document for read access.
    '''

    def __init__(self, content):
        self._content = content

    def get_content(self):
        '''Returns the whole content of the document.'''
        return {'all': self._content}


class DocumentIndex(object):

    '''
    Class containing the indexing result for one document.
    If provided with a indexConfig, the indexing will parse the document
    and filter stop words. Otherwise, indexing will be done on 
    the whole content.
    '''

    def __init__(self, content, indexConfig=None):
        self.word_count = {}
        self._maxword_count = -1
        if indexConfig:
            self._config = indexConfig
            self._doc = CACMStructuredDocument(content, indexConfig)
        else:
            self._config = None
            self._doc = PlainDocument(content)
        self._init_index()

    def get_word_count(self):
        '''Returns a dictionary with words and their counts.'''
        return self.word_count

    def _init_index(self):
        '''Indexes one document and populates word_count.'''
        doc_content = self._doc.get_content()
        for field in doc_content:
            field_content = doc_content[field]
            field_wc = self._compute_word_count(field_content)
            self.word_count = merge_dictionaries(self.word_count, field_wc)

    def _compute_word_count(self, field_content):
        '''Computes the word count for a string.'''
        return count_tokens(self._tokenize(field_content))

    def _tokenize(self, content):
        '''Returns an array of tokens (clean words) in a string.'''
        if not self._config:
            stop_words = []
        else:
            stop_words = self._config.stop_words
        tokens = get_word_list(content, stop_words)
        return tokens
