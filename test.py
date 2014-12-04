from indexing import Index
from indexing import DocumentIndex

index = Index("data/cacm.all")



doc = DocumentIndex(index.getDocumentContent(1))

print(doc.getFieldContent(".X"))
