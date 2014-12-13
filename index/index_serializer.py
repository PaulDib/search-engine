import pickle

class IndexSerializer:
    @staticmethod
    def saveToFile(index, file):
        fp = open(file, 'wb')
        pickle.dump(index, fp)
        fp.close()

    @staticmethod
    def loadFromFile(file):
        fp = open(file, 'rb')
        index = pickle.load(fp)
        fp.close()
        return index
