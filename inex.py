import os
from index.core import Index, IndexSerializer
from index.core.document_parser import INEXDocumentParser
import time

file_paths = ['../inex2007/documents/' + x for x in os.listdir('../inex2007/documents/')]
print(len(file_paths))

start_time = time.time()
index = Index(file_paths, 'data/common_words', parser_type=INEXDocumentParser)
print("indexing took {0} seconds".format(time.time() - start_time))

IndexSerializer.save_to_file(index, 'index_inex.idx')