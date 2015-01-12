from index.core import IndexConfig, Index

config = IndexConfig('data/common_words')
config.fields = ['<name id="', '<body>']
config.focus_fields = ['<body>']
config.id_marker = '<name id="'

index = Index('../inex2007/documents/290.xml', config)
print(index._index)