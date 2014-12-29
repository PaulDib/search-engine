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
        expected = {
            'algebraic': {'count': 1, 'norm_count': 0.5},
            'international': {'count': 1, 'norm_count': 0.5},
            'language': {'count': 1, 'norm_count': 0.5},
            'preliminary': {'count': 2, 'norm_count': 1.0},
            'report': {'count': 1, 'norm_count': 0.5}
        }
        self.assertEqual(expected, self.docIndex.getWordCount())

    def test_getTitle(self):
        expected = "Preliminary Report-International Algebraic Language preliminary"
        self.assertEqual(expected, self.doc.getTitle())

    def test_documentIndex_plainText(self):
        ''' Test document indexing with a plain text document.'''
        plainText = "a b a"
        docIdx = DocumentIndex(plainText)
        expected = { "a" : {'count': 2, 'norm_count': 1.0}, "b": {'count': 1, 'norm_count': 0.5} }
        self.assertEqual(expected, docIdx.getWordCount())

    def test_PlainDocument_getFocusContent(self):
        plainText = "a b a"
        plainDoc = PlainDocument(plainText)
        self.assertEqual(plainText, plainDoc.getFocusContent()['all'])
