import pickle

class IndexSerializer:
    @staticmethod
    def saveToFile(index, file):
        fp = open(file, 'w')
        pickle.dump(index, fp)
        fp.close()

    @staticmethod
    def loadFromFile(file):
        fp = open(file, 'r')
        idx = pickle.load(fp)
        fp.close()
        return idx
