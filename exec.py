from index.index_config import IndexConfig
from index.index import Index
from index.index_serializer import IndexSerializer
from index.boolean_query import BooleanQuery
import os

if os.path.isfile('index.idx'):
    index = IndexSerializer.loadFromFile('index.idx')
else:
    config = IndexConfig("data/common_words")
    index = Index("data/cacm.all", config)
    IndexSerializer.saveToFile(index, 'index.idx')

query = BooleanQuery("algebraic * (language + !expression)")
results = query.execute(index)
print(results)
