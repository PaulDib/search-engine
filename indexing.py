class Index:
    """Class containing the whole index: documents and the lists of frequencies"""
    def __init__(self, dataFiles):
        self.dataFiles = dataFiles
        self.documentLocations = {}
        self.idMarker = ".I"
        self.locateDocuments()

    def locateDocuments(self):
        if isinstance(self.dataFiles, str):
            self.readDocIdsInFile(self.dataFiles)
        elif  type(self.dataFiles) is list:
            for file in self.dataFiles:
                self.readDocIdsInFile(file)
        else:
            raise TypeError("dataFiles should be a string or a list")

    def readDocIdsInFile(self, file):
        """Populating a dictionary { docId: { file: filePath, start: startPos, end: endPos } } for each document."""
        with open(file) as f:
            lines = f.readlines()
            i = 0
            previousDocId = None
            for line in lines:
                if line.startswith(self.idMarker):
                    docId = int(line[len(self.idMarker):])
                    if previousDocId != None:
                        self.documentLocations[previousDocId]["end"] = i - 1
                    dic = { "file": file, "start": i, "end": None }
                    self.documentLocations[docId] = dic
                    previousDocId = docId
                i = i + 1
            if previousDocId != None:
                self.documentLocations[previousDocId]["end"] = i - 1

    def getDocumentContent(self, docId):
        """Outputs the document content"""
        if docId in self.documentLocations:
            content = []
            docInfo = self.documentLocations[docId]
            with open(docInfo["file"]) as f:
                for i, line in enumerate(f):
                    if i >= docInfo["start"] and i <= docInfo["end"]:
                        content = content + [line]
            return content
        raise ValueError("doc "+ docId + " not found")

class DocumentIndex:
    """Class containing the indexing result for one document"""
    def __init__(self, content):
        self.fields = [".I", ".T", ".W", ".K", ".B", ".A", ".N", ".X",".K"]
        self.focusFields = [".T", ".W", ".K"]
        self.getFieldPositions(content)
        self.createIndex(content)

    def getFieldPositions(self, content):
        self.fieldPositions = {}
        for field in self.fields:
            self.fieldPositions[field] = next((i for (i, x) in content if x == field), -1)

    def createIndex(self, content):
        for field in fields:
            fieldContent = self.getFieldContent(field, content)

    def getFieldContent(self, field, documentContent):
        startPos = self.fieldPositions[field] + 1
        stopPos = min({k:v for (k,v) in self.fieldPositions.iteritems() if v > startPos})
        return content[startPos:stopPos].join()
