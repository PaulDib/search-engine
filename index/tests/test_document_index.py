import unittest
import os
from index.document_index import DocumentIndex, StructuredDocument, PlainDocument
from index.index_config import IndexConfig

class DocumentIndexTests(unittest.TestCase):
    def setUp(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + "/test_data") as file:
            self.testContent = file.read().splitlines()
        self.docIndex = DocumentIndex(self.testContent, IndexConfig())
        self.doc = StructuredDocument(self.testContent, IndexConfig())

    def test_getFieldPositions(self):
        expected = {'.A': 5, '.B': 3, '.I': 0, '.K': -1, '.N': 8, '.T': 1, '.W': -1, '.X': 10}
        actual = self.doc.fieldPositions
        self.assertEqual(expected, actual)

    def test_structuredDocument_getAllContent(self):
        expected = "Perlis, A. J.\nSamelson,K."
        actual = self.doc.getAllContent()['.A']
        self.assertEqual(expected, actual)

    def test_createIndex(self):
        expected = {'report': 1, 'international': 1, 'algebraic': 1, 'language': 1, 'preliminary': 2}
        self.assertEqual(expected, self.docIndex.getWordCount())

    def test_getTitle(self):
        expected = "Preliminary Report-International Algebraic Language preliminary"
        self.assertEqual(expected, self.doc.getTitle())

    def test_documentIndex_plainText(self):
        ''' Test document indexing with a plain text document.'''
        plainText = "a b a"
        docIdx = DocumentIndex(plainText)
        expected = { "a" : 2, "b": 1 }
        self.assertEqual(expected, docIdx.getWordCount())

    def test_PlainDocument_getFocusContent(self):
        plainText = "a b a"
        plainDoc = PlainDocument(plainText)
        self.assertEqual(plainText, plainDoc.getFocusContent()['all'])
