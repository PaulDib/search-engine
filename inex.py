import os, sys
from index.core import Index, IndexSerializer
from index.core.document_parser import INEXDocumentParser
import time
from multiprocessing import freeze_support
from pympler.asizeof import asizeof

if __name__ == '__main__':
    freeze_support()
    file_paths = ['../inex2007/train_parts/documents/' + x for x in os.listdir('../inex2007/train_parts/documents/')]
    print(len(file_paths))

    start_time = time.time()
    index = Index(file_paths, 'data/common_words', parser_type=INEXDocumentParser)
    print("indexing took {0} seconds".format(time.time() - start_time))
    print("vocabulary size: {0} words".format(len(index._inverted_index)))
    print("size of index {0}".format(asizeof(index)))
    print(len(index._index))
    IndexSerializer.save_to_file(index, 'index_inex.idx')


