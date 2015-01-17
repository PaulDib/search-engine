import unittest
from ..dictionary_as_string import DictionaryAsString


class DictionaryAsStringTests(unittest.TestCase):
    def test_create_empty(self):
        dic = DictionaryAsString()
        self.assertEqual(0, len(dic))

    def test_add_item(self):
        dic = DictionaryAsString()
        dic["word"] = 5

        self.assertEqual(1, len(dic))

        dic["wordagain"] = 5
        self.assertEqual(2, len(dic))

    def test_change_item_value(self):
        dic = DictionaryAsString()
        dic["word"] = 1
        dic["word"] = 2

        self.assertEqual(1, len(dic))
        self.assertEqual(2, dic["word"])

    def test_get_item(self):
        dic = DictionaryAsString()
        dic["word"] = 1

        self.assertEqual(1, dic["word"])

    def test_contains_true(self):
        dic = DictionaryAsString()
        dic["word"] = 1

        self.assertEqual(True, "word" in dic)

    def test_contains_false(self):
        dic = DictionaryAsString()
        dic["word"] = 1

        self.assertEqual(False, "wordagain" in dic)
