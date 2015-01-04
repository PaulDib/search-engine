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

    def test_flatten_single_depth(self):
        dic = {"a": { "b" : [0, 1, 2], "c": 1 }}
        flat = {"a.b": [0, 1, 2], "a.c": 1}
        self.assertEqual(flat, flatten(dic))

    def test_flatten_multiple_depth(self):
        dic = {"a": { "b" : [0, 1, 2], "c": 1 }, "d": {"e": {"f": 5, "g": True}}}
        flat = {"a.b": [0, 1, 2], "a.c": 1, "d.e.f": 5, "d.e.g": True}
        self.assertEqual(flat, flatten(dic))

    def test_tf_idf_simple_values(self):
        self.assertEqual(0, tf_idf(0, 5, 10))
        self.assertEqual(0, tf_idf(1, 1, 1))

    def test_norm(self):
        vectorA = {'a' : { 'count': 0.5 }, 'b' : { 'count': 0.5 }, 'c' : { 'count': 0.5 }, 'd' : { 'count': 0.5 }}
        self.assertEqual(1.0, norm(vectorA, 'count'))
