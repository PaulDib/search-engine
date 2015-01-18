import os
import time
from multiprocessing import freeze_support
from pympler.asizeof import asizeof
from index.core import Index, IndexSerializer, Configuration
from index.core.document_parser import INEXDocumentParser
from index.core.dictionary_as_string import DictionaryAsString


# Setting up the index package for the feast.
Configuration.IndexDict = DictionaryAsString
Configuration.DocumentParser = INEXDocumentParser
Configuration.number_of_threads = 8

# Path to folder containing the documents to eat.
FOLDER_PATH = '../inex2007/train_parts/documents/'


if __name__ == '__main__':
    freeze_support()
    FILE_PATHS = [FOLDER_PATH + x for x in os.listdir(FOLDER_PATH)]
    print("{0} files found".format(len(FILE_PATHS)))

    START_TIME = time.time()
    INDEX = Index(FILE_PATHS, 'data/common_words')
    print("indexing took {0} seconds".format(time.time() - START_TIME))
    print("vocabulary size: {0} words".format(len(INDEX._inverted_index)))
    print("size of index: {0} bytes".format(asizeof(INDEX)))
    print("{0} files indexed".format(len(INDEX._index)))
    IndexSerializer.save_to_file(INDEX, 'index_inex.idx')
