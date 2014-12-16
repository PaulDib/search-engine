from .document_index import DocumentIndex

class VectorialQuery:
    def __init__(self, query):
        self._query = query
        self._initIndex()

    def _initIndex(self):
        docIdx = DocumentIndex(self._query)
        self._index = docIdx.getWordCount()

    def execute(self, index):
        result_dict = index.getMatchingDocuments(self._index)
        sorted_results = sorted(result_dict.items(),
                                key = lambda x: x[1],
                                reverse = True)
        return sorted_results
