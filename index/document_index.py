from .utility import *

class DocumentIndex:
    '''Class containing the indexing result for one document.'''
    def __init__(self, content, indexConfig):
        self._config = indexConfig
        self.wordCount = {}
        self._getFieldPositions(content)
        self._initIndex(content)
        
    def getWordCount(self):
        return self.wordCount

    def getFieldContent(self, field, documentContent):
        startPos = self.fieldPositions[field] + 1
        if (startPos <= 0):
            return ""
        nextFields = {v for (k,v) in self.fieldPositions.items() if v > startPos}
        stopPos = min(nextFields) if nextFields else len(documentContent)
        return "\n".join(documentContent[startPos:stopPos])

    def _getFieldPositions(self, content):
        '''Populates fieldPositions = { 'fieldName': startPosition } dictionary.'''
        self.fieldPositions = {}
        for field in self._config.fields:
            self.fieldPositions[field] = next((i for i, l in enumerate(content) if l.startswith(field)), -1)

    def _initIndex(self, content):
        for field in self._config.focusFields:
            self.wordCount = mergeDictionaries(self.wordCount, self._getWordCount(field, content))

    def _getWordCount(self, field, content):
        fieldContent = self.getFieldContent(field, content)
        return countTokens(self._tokenize(fieldContent))

    def _tokenize(self, content):
        tokens = getWordList(content)
        tokens = filterWords(tokens, self._config.stopWords)
        return tokens
