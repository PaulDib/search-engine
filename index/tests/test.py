"""from indexing import Index
from indexing import DocumentIndex

index = Index("data/cacm.all")



doc = DocumentIndex(index.getDocumentContent(1))

print(doc.getFieldContent(".X"))
"""
import unittest
import os
from index.index import DocumentIndex

class DocumentIndexTests(unittest.TestCase):
    def setUp(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + "/test_data") as file:
            self.testContent = file.read().splitlines()
            self.docIndex = DocumentIndex(self.testContent)

    def testGetFieldPositions(self):
        expected = {'.A': 5, '.B': 3, '.I': 0, '.K': -1, '.N': 8, '.T': 1, '.W': -1, '.X': 10}
        actual = self.docIndex.fieldPositions
        self.assertEqual(expected, actual)

    def testGetFieldContent(self):
        expected = "Perlis, A. J.\nSamelson,K."
        actual = self.docIndex.getFieldContent(".A", self.testContent)
        self.assertEqual(expected, actual)
