import unittest
from index.utility import *

class UtilityTests(unittest.TestCase):
    def test_splitContent(self):
        testVal = "Should be split - around'special*chars-like,these.ones and around spaces"
        expected = ["Should", "be", "split", "around", "special", "chars", "like", "these" , "ones", "and", "around", "spaces"]
        self.assertEqual(expected, splitContent(testVal))

    def test_filterOutStopWords(self):
        testVal = ["Should", "be", "split", "around", "special", "chars", "like", "these" , "ones", "and", "around", "spaces"]
        expected = ["Should", "split", "special", "chars", "like", "these" , "ones", "and", "spaces"]
        self.assertEqual(expected, filterWords(testVal,  ["around", "be"]))

    def test_mergeDictionaries(self):
        a = { "key1": 4, "key2": 5 }
        b = { "key2": 4, "key3": 5 }
        expected = { "key1": 4, "key2": 9, "key3": 5 }
        self.assertEqual(expected, mergeDictionaries(a, b))
