from .document_index import DocumentIndex, StructuredDocument
from .utility import mergeDictionaries, tf_idf, norm
from .constants import *

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
        return StructuredDocument(self._getDocumentContent(docId), self._config)

    def indexByDocId(self, docId):
        '''Returns a dictionary of words with their frequency in a document'''
        return self._index[docId] if docId in self._index else {}

    def getMatchingDocuments(self, documentWords, weight_key = NORM_TFIDF):
        '''
        Returns documents similar to the input by computing the cosine of the
        input document to the collection.
        '''
        results = {}
        for word in documentWords:
            if word in self._invertedIndex:
                weight_input = tf_idf(documentWords[word][COUNT],
                                    self._documentFrequencies[word],
                                    self._number_of_docs)
                documentWords[word][weight_key] = weight_input
                for doc in self._invertedIndex[word]:
                    docId = doc[DOCID]
                    weight_doc = doc[weight_key]
                    if docId in results:
                        results[docId] = results[docId] + weight_doc*weight_input
                    else:
                        results[docId] = weight_doc*weight_input
        queryNorm = norm(documentWords, weight_key)
        for docId in results:
            resultNorm = norm(self._index[docId][WORDS], weight_key)
            results[docId] = results[docId] / (resultNorm*queryNorm)
        return results

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
        # TODO: Refactor
        self._documentFrequencies = {}
        self._number_of_docs = len(self._index)
        for word in self._invertedIndex:
            df = len(self._invertedIndex[word])
            self._documentFrequencies[word] = df
            for doc in self._invertedIndex[word]:
                tfidf = tf_idf(doc[COUNT], df, self._number_of_docs )
                doc[TFIDF] = tfidf
                self._index[doc[DOCID]][WORDS][word][TFIDF] = tfidf
            max_tfidf = max({doc[TFIDF] for doc in self._invertedIndex[word]})
            if max_tfidf > 0:
                for doc in self._invertedIndex[word]:
                    doc[NORM_TFIDF] = doc[TFIDF] / max_tfidf
                    self._index[doc[DOCID]][WORDS][word][NORM_TFIDF] = doc[TFIDF] / max_tfidf
            else:
                for doc in self._invertedIndex[word]:
                    doc[NORM_TFIDF] = doc[TFIDF]
                    self._index[doc[DOCID]][WORDS][word][NORM_TFIDF] = doc[TFIDF]

    def _saveDocumentLocation(self, docId, file, startPos, endPos):
        '''Saves the position of the document in its file for later reads.'''
        self._index[docId] = { FILE: file, START: startPos, END: endPos }

    def _addDocumentToIndex(self, docId, content):
        '''Populating the index with the result for one document.'''
        wordCount = DocumentIndex(content, self._config).getWordCount()
        self._index[docId][WORDS] = wordCount
        invertedWords = { word: [{DOCID: docId, COUNT: wordCount[word][COUNT], NORM_COUNT:  wordCount[word][NORM_COUNT]}]
            for word in wordCount if wordCount[word][COUNT] > 0 }
        self._invertedIndex = mergeDictionaries(self._invertedIndex, invertedWords)

    def _getDocumentContent(self, docId):
        '''Outputs the document content as a list of lines'''
        if docId in self._index:
            content = []
            docInfo = self._index[docId]
            with open(docInfo[FILE]) as f:
                for i, line in enumerate(f):
                    if i >= docInfo[START] and i <= docInfo[END]:
                        content = content + [line]
            return content
        raise ValueError("doc "+ docId + " not found")
