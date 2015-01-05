'''
Configuration object for an index.
'''

class IndexConfig(object):
    '''Class containing the configuration items for the index'''
    def __init__(self, stop_word_file=""):
        if stop_word_file:
            self.read_stop_words(stop_word_file)
        else:
            self.stop_words = []
        self.fields = [".I", ".T", ".W", ".K", ".B", ".A", ".N", ".X", ".K"]
        self.focus_fields = [".T", ".W", ".K"]
        self.id_marker = ".I"
        self.title_field = ".T"

    def read_stop_words(self, stop_word_file):
        '''
        Read a file containing stop words and populates the stop word list.'''
        with open(stop_word_file) as file_ptr:
            self.stop_words = file_ptr.read().splitlines()
