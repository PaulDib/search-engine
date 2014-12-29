from .utility import *
import re

class StructuredDocument:
    '''
    Class representing one structured document for read access.
    '''
    def __init__(self, content, indexConfig):
        self._config = indexConfig
        self._content = content
        self._getFieldPositions()

    def getFocusContent(self):
        res = {}
        for field in self._config.focusFields:
            res[field] = self._getFieldContent(field)
        return res

    def getAllContent(self):
        res = {}
        for field in self._config.fields:
            res[field] = self._getFieldContent(field)
        return res

    def getTitle(self):
        result = self._getFieldContent(self._config.titleField).strip()
        result = re.sub(r'(\s)+', r' ', result)
        return result

    def _getFieldContent(self, field):
        startPos = self.fieldPositions[field] + 1
        if (startPos <= 0):
            return ""
        nextFields = {v for (k,v) in self.fieldPositions.items() if v > startPos}
        stopPos = min(nextFields) if nextFields else len(self._content)
        return "\n".join(self._content[startPos:stopPos])

    def _getFieldPositions(self):
        '''Populates fieldPositions = { 'fieldName': startPosition } dictionary.'''
        self.fieldPositions = {}
        for field in self._config.fields:
            self.fieldPositions[field] = next((i for i, l in enumerate(self._content) if l.startswith(field)), -1)


class PlainDocument:
    '''
    Class representing a plain text (non structured) document for read access.
    '''
    def __init__(self, content):
        self._content = content

    def getAllContent(self):
        return { 'all' : self._content }

    def getFocusContent(self):
        return self.getAllContent()


class DocumentIndex:
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
        docContent = self._doc.getFocusContent()
        for field in docContent:
            fieldContent = docContent[field]
            field_wc = self._computeWordCount(fieldContent)
            self.wordCount = mergeDictionaries(self.wordCount, field_wc)
            field_max = max(field_wc.values()) if field_wc else -1
            self._maxWordCount = field_max if field_max > self._maxWordCount else self._maxWordCount
        self.wordCount = { word: {'count': count, 'norm_count': count/self._maxWordCount } for word, count in self.wordCount.items() }

    def _computeWordCount(self, fieldContent):
        return countTokens(self._tokenize(fieldContent))

    def _tokenize(self, content):
        tokens = getWordList(content)
        if self._config:
            tokens = filterWords(tokens, self._config.stopWords)
        return tokens
