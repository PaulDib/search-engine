from .utility import *

class Document:
    '''
    Class representing one document for read access.
    '''
    def __init__(self, content, indexConfig):
        self._config = indexConfig
        self._content = content
        self._getFieldPositions()

    def getFieldContent(self, field):
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


class DocumentIndex:
    '''
    Class containing the indexing result for one document.
    '''
    def __init__(self, content, indexConfig):
        self._config = indexConfig
        self.wordCount = {}
        self._doc = Document(content, indexConfig)
        self._initIndex()

    def getWordCount(self):
        return self.wordCount

    def _initIndex(self):
        for field in self._config.focusFields:
            self.wordCount = mergeDictionaries(self.wordCount, self._getWordCount(field))

    def _getWordCount(self, field):
        fieldContent = self._doc.getFieldContent(field)
        return countTokens(self._tokenize(fieldContent))

    def _tokenize(self, content):
        tokens = getWordList(content)
        tokens = filterWords(tokens, self._config.stopWords)
        return tokens
