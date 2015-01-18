'''
Configuration items for the index package.
'''
from nltk import PorterStemmer
from .document_parser import CACMDocumentParser


class FakeStemmer:
    def __init__(self):
        pass

    def stem_word(self, word):
        '''Doesn't really stem anything.'''
        return word


class Configuration(object):

    '''Exposes configuration items for the index core package.'''

    number_of_threads = 1
    DocumentParser = CACMDocumentParser
    IndexDict = dict
    stemmer = PorterStemmer()