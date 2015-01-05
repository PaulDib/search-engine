'''
Provides classes to index single documents.
'''
from .utility import getWordList, countTokens, mergeDictionaries, filterWords
from .constants import COUNT, NORM_COUNT
import re

class StructuredDocument(object):
    '''
    Class representing one structured document for read access.
    '''
    def __init__(self, content, indexConfig):
        self._config = indexConfig
        self._content = content
        self.field_positions = {}
        self._get_field_positions()

    def get_focus_content(self):
        res = {}
        for field in self._config.focusFields:
            res[field] = self._get_field_content(field)
        return res

    def get_all_content(self):
        res = {}
        for field in self._config.fields:
            res[field] = self._get_field_content(field)
        return res

    def get_title(self):
        result = self._get_field_content(self._config.titleField).strip()
        result = re.sub(r'(\s)+', r' ', result)
        return result

    def _get_field_content(self, field):
        start_pos = self.field_positions[field] + 1
        if start_pos <= 0:
            return ""
        next_fields = {v \
            for (k, v) in self.field_positions.items() if v > start_pos}
        stop_pos = min(next_fields) if next_fields else len(self._content)
        return "\n".join(self._content[start_pos:stop_pos])

    def _get_field_positions(self):
        '''
        Populates field_positions = { 'fieldName': start_position } dictionary.
        '''
        self.field_positions = {}
        for field in self._config.fields:
            self.field_positions[field] = next((i for i, l \
                in enumerate(self._content) if l.startswith(field)), -1)


class PlainDocument(object):
    '''
    Class representing a plain text (non structured) document for read access.
    '''
    def __init__(self, content):
        self._content = content

    def get_all_content(self):
        return { 'all' : self._content }

    def get_focus_content(self):
        return self.get_all_content()


class DocumentIndex(object):
    '''
    Class containing the indexing result for one document.
    If provided with a indexConfig, the indexing will parse the document
    and filter stop words. Otherwise, it will be done on the whole content.
    '''
    def __init__(self, content, indexConfig = None):
        self.wordCount = {}
        self._maxWordCount = -1
        if indexConfig:
            self._config = indexConfig
            self._doc = StructuredDocument(content, indexConfig)
        else:
            self._config = None
            self._doc = PlainDocument(content)
        self._initIndex()

    def getWordCount(self):
        return self.wordCount

    def _initIndex(self):
        docContent = self._doc.get_focus_content()
        for field in docContent:
            fieldContent = docContent[field]
            field_wc = self._computeWordCount(fieldContent)
            self.wordCount = mergeDictionaries(self.wordCount, field_wc)
            field_max = max(field_wc.values()) if field_wc else -1
            self._maxWordCount = field_max if field_max > self._maxWordCount else self._maxWordCount
        self.wordCount = { word: { COUNT: count, NORM_COUNT: count/self._maxWordCount } for word, count in self.wordCount.items() }

    def _computeWordCount(self, fieldContent):
        return countTokens(self._tokenize(fieldContent))

    def _tokenize(self, content):
        tokens = getWordList(content)
        if self._config:
            tokens = filterWords(tokens, self._config.stopWords)
        return tokens
