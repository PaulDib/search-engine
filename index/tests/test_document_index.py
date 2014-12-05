import unittest
import os
from index.document_index import DocumentIndex
from index.index_config import IndexConfig

class DocumentIndexTests(unittest.TestCase):
    def setUp(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + "/test_data") as file:
            self.testContent = file.read().splitlines()
        self.docIndex = DocumentIndex(self.testContent, IndexConfig())

    def test_getFieldPositions(self):
        expected = {'.A': 5, '.B': 3, '.I': 0, '.K': -1, '.N': 8, '.T': 1, '.W': -1, '.X': 10}
        actual = self.docIndex.fieldPositions
        self.assertEqual(expected, actual)

    def test_getFieldContent(self):
        expected = "Perlis, A. J.\nSamelson,K."
        actual = self.docIndex.getFieldContent(".A", self.testContent)
        self.assertEqual(expected, actual)

    def test_splitContent_spaces(self):
        testVal = "Should be split around spaces"
        expected = ["Should", "be", "split", "around", "spaces"]
        self.assertEqual(expected, DocumentIndex.splitContent(testVal))

    def test_splitContent_specialChars(self):
        testVal = "Should be split - around'special*chars-like,these.ones around spaces"
        expected = ["Should", "be", "split", "around", "special", "chars", "like", "these" , "ones", "around", "spaces"]
        self.assertEqual(expected, DocumentIndex.splitContent(testVal))

    def test_filterOutStopWords(self):
        testVal = ["Should", "be", "split", "around", "special", "chars", "like", "these" , "ones", "around", "spaces"]
        expected = ["Should", "split", "special", "chars", "like", "these" , "ones", "spaces"]
        self.assertEqual(expected, DocumentIndex.filterWords(testVal,  ["around", "be"]))

    def test_createIndex(self):
        expected = {'report': 1, 'international': 1, 'algebraic': 1, 'language': 1, 'preliminary': 2}
        self.assertEqual(expected, self.docIndex.wordCount)

    def test_mergeDictionaries(self):
        a = { "key1": 4, "key2": 5 }
        b = { "key2": 4, "key3": 5 }
        expected = { "key1": 4, "key2": 9, "key3": 5 }
        self.assertEqual(expected, DocumentIndex.mergeDictionaries(a, b))
