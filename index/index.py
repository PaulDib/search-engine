from document_index import DocumentIndex
from utility import mergeDictionaries

class Index:
    '''Class containing the whole index: documents and the lists of frequencies'''
    def __init__(self, dataFiles, indexConfig):
        self._config = indexConfig
        self._dataFiles = dataFiles
        self._locateDocuments()
        self._initIndex()

    def search(self, word):
        '''Returns a list of docIds containing the requested word.'''
        stdWord = word.lower()
        return self._invertedIndex[stdWord] if stdWord in self._invertedIndex else []

    def documentById(self, docId):
        '''Returns a dictionary of words with their frequency in a document'''
        return self._index[docId] if docId in self._index else {}œ

    def _initIndex(self):
        self._invertedIndex = {}
        for docId in self._index:
            docIndex = DocumentIndex(self._getDocumentContent(docId), self._config)
            wordCount = docIndex.getWordCount()
            self._index[docId]['words'] = wordCount
            invertedWords = { word: [{'docId': docId, 'count': wordCount[word]}] for word in wordCount if wordCount[word] > 0 }
            self._invertedIndex = mergeDictionaries(self._invertedIndex, invertedWords)

    def _locateDocuments(self):
        '''Populating a dictionary locating each document in the different data files.'''
        self._index = {}
        if isinstance(self._dataFiles, str):
            self._readDocIdsInFile(self._dataFiles)
        elif  type(self._dataFiles) is list:
            for file in self._dataFiles:
                self._readDocIdsInFile(file)
        else:
            raise TypeError("dataFiles should be a string or a list")

    def _readDocIdsInFile(self, file):
        '''Populating a dictionary { docId: { file: filePath, start: startPos, end: endPos } } for each document.'''
        with open(file) as f:
            lines = f.readlines()
            i = 0
            previousDocId = None
            for line in lines:
                if line.startswith(self._config.idMarker):
                    docId = int(line[len(self._config.idMarker):])
                    if previousDocId != None:
                        self._index[previousDocId]["end"] = i - 1
                    dic = { "file": file, "start": i, "end": None }
                    self._index[docId] = dic
                    previousDocId = docId
                i = i + 1
            if previousDocId != None:
                self._index[previousDocId]["end"] = i - 1

    def _getDocumentContent(self, docId):
        '''Outputs the document content as a list of lines'''
        if docId in self._index:
            content = []
            docInfo = self._index[docId]
            with open(docInfo["file"]) as f:
                for i, line in enumerate(f):
                    if i >= docInfo["start"] and i <= docInfo["end"]:
                        content = content + [line]
            return content
        raise ValueError("doc "+ docId + " not found")
