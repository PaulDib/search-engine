from .document_index import DocumentIndex, StructuredDocument
from .utility import mergeDictionaries, tf_idf

class Index:
    '''
    Class containing the whole index: documents and the lists of frequencies
    '''
    def __init__(self, dataFiles, indexConfig):
        self._config = indexConfig
        self._dataFiles = dataFiles
        self._index = {}
        self._invertedIndex = {}
        self._initIndex()

    def search(self, word):
        '''Returns a list of docIds containing the requested word.'''
        stdWord = word.lower()
        return self._invertedIndex[stdWord] if stdWord in self._invertedIndex else []

    def documentById(self, docId):
        '''Returns a Document object for a requested doc id.'''
        return Document(self._getDocumentContent(docId), self._config)

    def indexByDocId(self, docId):
        '''Returns a dictionary of words with their frequency in a document'''
        return self._index[docId] if docId in self._index else {}

    def getAllDocIds(self):
        '''Returns a list with all doc ids in the index'''
        return [docId for docId in self._index]

    def _initIndex(self):
        if isinstance(self._dataFiles, str):
            self._indexFile(self._dataFiles)
        elif  type(self._dataFiles) is list:
            for file in self._dataFiles:
                self._indexFile(file)
        else:
            raise TypeError("dataFiles should be a string or a list")

        self._initStatistics()

    def _indexFile(self, file):
        '''Populating the index with the results for one file.'''
        with open(file) as f:
            docId = None
            documentContent = []
            for i, line in enumerate(f):
                if line.startswith(self._config.idMarker):
                    if docId != None:
                        # Indexing previous document
                        self._saveDocumentLocation(docId, file, documentStartPos, i - 1)
                        self._addDocumentToIndex(docId, documentContent)
                    docId = int(line[len(self._config.idMarker):])
                    documentStartPos = i
                    documentContent = []
                documentContent = documentContent + [line]

            # Handling last document.
            if docId != None:
                self._saveDocumentLocation(docId, file, documentStartPos, i - 1)
                self._addDocumentToIndex(docId, documentContent)

    def _initStatistics(self):
        number_of_docs = len(self._index)
        for word in self._invertedIndex:
            df = len(self._invertedIndex[word])
            for doc in self._invertedIndex[word]:
                tfidf = tf_idf(doc['count'], df, number_of_docs)
                doc['weight'] = tfidf

    def _saveDocumentLocation(self, docId, file, startPos, endPos):
        '''Saves the position of the document in its file for later reads.'''
        self._index[docId] = { "file": file, "start": startPos, "end": endPos }

    def _addDocumentToIndex(self, docId, content):
        '''Populating the index with the result for one document.'''
        wordCount = DocumentIndex(content, self._config).getWordCount()
        self._index[docId]['words'] = wordCount
        invertedWords = { word: [{'docId': docId, 'count': wordCount[word]}]
            for word in wordCount if wordCount[word] > 0 }
        self._invertedIndex = mergeDictionaries(self._invertedIndex, invertedWords)

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
