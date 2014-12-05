import re

class DocumentIndex:
    '''Class containing the indexing result for one document'''
    def __init__(self, content, indexConfig):
        self.__config = indexConfig
        self.wordCount = {}
        self.__getFieldPositions(content)
        self.__createIndex(content)

    def getFieldContent(self, field, documentContent):
        startPos = self.fieldPositions[field] + 1
        if (startPos <= 0):
            return ""
        nextFields = {v for (k,v) in self.fieldPositions.iteritems() if v > startPos}
        stopPos = min(nextFields) if nextFields else len(documentContent)
        return "\n".join(documentContent[startPos:stopPos])


    def __getFieldPositions(self, content):
        '''Populates fieldPositions = { 'fieldName': startPosition } dictionary.'''
        self.fieldPositions = {}
        for field in self.__config.fields:
            self.fieldPositions[field] = next((i for i, l in enumerate(content) if l.startswith(field)), -1)

    def __createIndex(self, content):
        for field in self.__config.focusFields:
            self.wordCount = DocumentIndex.mergeDictionaries(self.wordCount, self.__getWordCount(field, content))

    def __getWordCount(self, field, content):
        fieldContent = self.getFieldContent(field, content)
        return DocumentIndex.countTokens(self.__tokenize(fieldContent))

    def __tokenize(self, content):
        tokens = self.getWordList(content)
        tokens = DocumentIndex.filterWords(tokens, self.__config.stopWords)
        return tokens

    @staticmethod
    def filterWords(wordList, stopWords):
        return [x for x in wordList if x not in stopWords]

    @staticmethod
    def splitContent(content):
        '''Splits a string around spaces and non-alphanumeric characters'''
        return re.findall(r"[\w]+", content)

    @staticmethod
    def mergeDictionaries(a, b):
        '''Merge two dictionaries by summing values'''
        res = a
        for k in b:
            if k in res:
                res[k] = res[k] + b[k]
            else:
                res[k] = b[k]
        return res

    @staticmethod
    def getWordList(content):
        '''Gets the list of words in a string'''
        wordList = DocumentIndex.splitContent(content)
        wordList = [x.lower() for x in wordList]
        return wordList

    @staticmethod
    def countTokens(tokens):
        '''Given a list of elements, counts the number of occurences of each element as a dictionary.'''
        tokens = map(lambda x: { x: 1 }, tokens)
        return reduce(DocumentIndex.mergeDictionaries, tokens, {})
