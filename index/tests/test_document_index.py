import unittest
import os
from index.document_index import DocumentIndex, StructuredDocument, PlainDocument
from index.index_config import IndexConfig
from index.constants import *

class DocumentIndexTests(unittest.TestCase):
    def setUp(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + "/test_data") as file:
            self.testContent = file.read().splitlines()
        self.docIndex = DocumentIndex(self.testContent, IndexConfig())
        self.doc = StructuredDocument(self.testContent, IndexConfig())

    def test_get_field_positions(self):
        expected = {'.A': 5, '.B': 3, '.I': 0, '.K': -1, '.N': 8, '.T': 1, '.W': -1, '.X': 10}
        actual = self.doc.field_positions
        self.assertEqual(expected, actual)

    def test_structuredDocument_get_all_content(self):
        expected = "Perlis, A. J.\nSamelson,K."
        actual = self.doc.get_all_content()['.A']
        self.assertEqual(expected, actual)

    def test_createIndex(self):
        expected = {
            'algebraic': {COUNT: 1, NORM_COUNT: 0.5},
            'international': {COUNT: 1, NORM_COUNT: 0.5},
            'language': {COUNT: 1, NORM_COUNT: 0.5},
            'preliminary': {COUNT: 2, NORM_COUNT: 1.0},
            'report': {COUNT: 1, NORM_COUNT: 0.5}
        }
        self.assertEqual(expected, self.docIndex.getWordCount())

    def test_get_title(self):
        expected = "Preliminary Report-International Algebraic Language preliminary"
        self.assertEqual(expected, self.doc.get_title())

    def test_documentIndex_plainText(self):
        ''' Test document indexing with a plain text document.'''
        plainText = "a b a"
        docIdx = DocumentIndex(plainText)
        expected = { "a" : {COUNT: 2, NORM_COUNT: 1.0}, "b": {COUNT: 1, NORM_COUNT: 0.5} }
        self.assertEqual(expected, docIdx.getWordCount())

    def test_PlainDocument_get_focus_content(self):
        plainText = "a b a"
        plainDoc = PlainDocument(plainText)
        self.assertEqual(plainText, plainDoc.get_focus_content()['all'])
