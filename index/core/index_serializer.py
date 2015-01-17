'''
Allow to save an index to a file or read a saved index.
'''
import pickle


class IndexSerializer(object):

    '''
    Allow to save an index to a file or read a saved index.
    '''

    def __init__(self):
        pass

    @staticmethod
    def save_to_file(index, file_path):
        '''
        Save the index to the specified file.
        '''
        file_ptr = open(file_path, 'wb')
        index._inverted_index = []
        pickle.dump(index, file_ptr, protocol=4)
        file_ptr.close()

    @staticmethod
    def load_from_file(file_path):
        '''
        Load and returns and index from a file.
        '''
        file_ptr = open(file_path, 'rb')
        index = pickle.load(file_ptr)
        index._inverted_index = index._invert_index(index._index)
        file_ptr.close()
        return index
