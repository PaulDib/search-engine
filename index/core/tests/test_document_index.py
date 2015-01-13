import unittest
import os
from ..document_index import DocumentIndex, PlainDocument
from ..document_parser import CACMDocumentParser, INEXDocumentParser


class DocumentIndexTests(unittest.TestCase):

    def setUp(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + "/test_data") as file:
            self.test_content = "\n".join(file.read().splitlines())
        with open(os.path.dirname(os.path.realpath(__file__)) + "/test_data_inex.xml") as file:
            self.test_inex = "\n".join(file.read().splitlines())
        self.doc = CACMDocumentParser().parse_document(self.test_content)
        self.doc_index = DocumentIndex(self.doc.get_content())

    def test_get_doc_id_inex(self):
        doc = INEXDocumentParser().parse_document(self.test_inex)
        self.assertEqual(290, doc.get_doc_id())

    def test_get_title_inex(self):
        '''Tests the get_title function.'''
        expected = "A"
        doc = INEXDocumentParser().parse_document(self.test_inex)
        self.assertEqual(expected, doc.get_title())

    def test_get_title(self):
        '''Tests the get_title function.'''
        expected = "Preliminary Report-International Algebraic Language preliminary"
        self.assertEqual(expected, self.doc.get_title())

    def test_create_index(self):
        expected = {
            'algebra': 1,
            'intern': 1,
            'languag': 1,
            'preliminari': 2,
            'report': 1
        }
        self.assertEqual(expected, self.doc_index.get_word_count())

    def test_document_index_plain_text(self):
        ''' Test document indexing with a plain text document.'''
        plain_text = "a b a"
        doc_idx = DocumentIndex(plain_text)
        expected = {
            "a": 2,
            "b": 1
        }
        self.assertEqual(expected, doc_idx.get_word_count())

    def test_document_index_plain_text_special_chars(self):
        ''' Test document indexing with a plain text document with special chars.'''
        plain_text = "a - b ? (a)"
        doc_idx = DocumentIndex(plain_text)
        expected = {"a": 2,
                    "b": 1}
        self.assertEqual(expected, doc_idx.get_word_count())

    def test_plain_document_get_content(self):
        plain_text = "a b a"
        plain_doc = PlainDocument(plain_text)
        self.assertEqual(plain_text, plain_doc.get_content())
