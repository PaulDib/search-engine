class Index:
    '''Class containing the whole index: documents and the lists of frequencies'''
    def __init__(self, dataFiles, indexConfig):
        self.config = indexConfig
        self.dataFiles = dataFiles
        self.documentLocations = {}
        self.locateDocuments()
        self.createInvertedIndex()

    def locateDocuments(self):
        '''Populating a dictionary locating each document in the different data files.'''
        if isinstance(self.dataFiles, str):
            self.readDocIdsInFile(self.dataFiles)
        elif  type(self.dataFiles) is list:
            for file in self.dataFiles:
                self.readDocIdsInFile(file)
        else:
            raise TypeError("dataFiles should be a string or a list")

    def readDocIdsInFile(self, file):
        '''Populating a dictionary { docId: { file: filePath, start: startPos, end: endPos } } for each document.'''
        with open(file) as f:
            lines = f.readlines()
            i = 0
            previousDocId = None
            for line in lines:
                if line.startswith(self.config.idMarker):
                    docId = int(line[len(self.config.idMarker):])
                    if previousDocId != None:
                        self.documentLocations[previousDocId]["end"] = i - 1
                    dic = { "file": file, "start": i, "end": None }
                    self.documentLocations[docId] = dic
                    previousDocId = docId
                i = i + 1
            if previousDocId != None:
                self.documentLocations[previousDocId]["end"] = i - 1

    def getDocumentContent(self, docId):
        '''Outputs the document content as a list of lines'''
        if docId in self.documentLocations:
            content = []
            docInfo = self.documentLocations[docId]
            with open(docInfo["file"]) as f:
                for i, line in enumerate(f):
                    if i >= docInfo["start"] and i <= docInfo["end"]:
                        content = content + [line]
            return content
        raise ValueError("doc "+ docId + " not found")
