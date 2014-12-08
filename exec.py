from index.index_config import IndexConfig
from index.index import Index
from index.index_serializer import IndexSerializer
import os

if os.path.isfile('index.idx'):
    index = IndexSerializer.loadFromFile('index.idx')
else:
    config = IndexConfig("data/common_words")
    index = Index("data/cacm.all", config)
    IndexSerializer.saveToFile(index, 'index.idx')

print(index._index[60])
print(index._invertedIndex['constraints'])
print(len(index._index))
print(len(index._invertedIndex))
