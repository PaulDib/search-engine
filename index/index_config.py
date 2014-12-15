class IndexConfig:
    '''Class containing the configuration items for the index'''
    def __init__(self, stopWordFile = ""):
        if stopWordFile:
            self.readStopWords(stopWordFile)
        else:
            self.stopWords = []
        self.fields = [".I", ".T", ".W", ".K", ".B", ".A", ".N", ".X",".K"]
        self.focusFields = [".T", ".W", ".K"]
        self.idMarker = ".I"
        self.titleField = ".T"

    def readStopWords(self, stopWordFile):
        with open(stopWordFile) as file:
            self.stopWords = file.read().splitlines()
