import unittest
import os
from ..document_index import DocumentIndex, StructuredDocument, PlainDocument
from ..index_config import IndexConfig
from ..constants import FILE, WORDS, START, END


class DocumentIndexTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + "/test_data") as file:
            self.test_content = file.read().splitlines()
        self.doc_index = DocumentIndex(self.test_content, IndexConfig())
        self.doc = StructuredDocument(self.test_content, IndexConfig())

    def test_get_field_positions(self):
        expected = {'.A': 5, '.B': 3, '.I': 0, '.K': -1,
                    '.N': 8, '.T': 1, '.W': -1, '.X': 10}
        actual = self.doc.field_positions
        self.assertEqual(expected, actual)

    def test_create_index(self):
        expected = {
            'algebra': 1,
            'intern': 1,
            'languag': 1,
            'preliminari': 2,
            'report': 1
        }
        self.assertEqual(expected, self.doc_index.get_word_count())

    def test_get_title(self):
        '''Tests the get_title function.'''
        expected = "Preliminary Report-International Algebraic Language preliminary"
        self.assertEqual(expected, self.doc.get_title())

    def test_document_index_plain_text(self):
        ''' Test document indexing with a plain text document.'''
        plain_text = "a b a"
        doc_idx = DocumentIndex(plain_text)
        expected = {
            "a": 2,
            "b": 1
        }
        self.assertEqual(expected, doc_idx.get_word_count())

    def test_document_index_plain_text_special_characters(self):
        ''' Test document indexing with a plain text document with special chars.'''
        plain_text = "a - b ? (a)"
        doc_idx = DocumentIndex(plain_text)
        expected = {"a": 2,
                    "b": 1}
        self.assertEqual(expected, doc_idx.get_word_count())

    def test_plain_document_get_content(self):
        plain_text = "a b a"
        plainDoc = PlainDocument(plain_text)
        self.assertEqual(plain_text, plainDoc.get_content()['all'])
