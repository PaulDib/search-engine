import unittest
import os
from ..boolean_query import OperatorNot, OperatorAnd, OperatorOr, OperatorNode, WordLeaf
from ..index import Index
from ..index_config import IndexConfig


class BooleanQueryTests(unittest.TestCase):

    def setUp(self):
        self._index = Index(
            os.path.dirname(os.path.realpath(__file__)) + "/test_data", IndexConfig())

    def test_BooleanQuery_Or_simple(self):
        '''Testing query results for "algrebraic + extraction"'''
        operands = [WordLeaf("algebraic"), WordLeaf("extraction")]
        root = OperatorNode(operator=OperatorOr, operands=operands)
        root.set_index(self._index)
        actual = root.get_postings()
        expected = {1, 2}
        self.assertEqual(expected, actual)

    def test_BooleanQuery_Or_redundancy(self):
        '''Testing query results for "language + extraction"'''
        operands = [WordLeaf("language"), WordLeaf("extraction")]
        root = OperatorNode(operator=OperatorOr, operands=operands)
        root.set_index(self._index)
        actual = root.get_postings()
        expected = {1, 2}
        self.assertEqual(expected, actual)

    def test_BooleanQuery_And_simple(self):
        '''Testing query results for "algrebraic * extraction"'''
        operands = [WordLeaf("algebraic"), WordLeaf("extraction")]
        root = OperatorNode(operator=OperatorAnd, operands=operands)
        root.set_index(self._index)
        actual = root.get_postings()
        expected = set()
        self.assertEqual(expected, actual)

    def test_BooleanQuery_And_no_results(self):
        '''Testing query results for "language * extraction"'''
        operands = [WordLeaf("language"), WordLeaf("extraction")]
        root = OperatorNode(operator=OperatorAnd, operands=operands)
        root.set_index(self._index)
        actual = root.get_postings()
        expected = {2}
        self.assertEqual(expected, actual)

    def test_BooleanQuery_Not_simple(self):
        '''Testing query results for "!algebraic"'''
        operands = [WordLeaf("algebraic")]
        root = OperatorNode(operator=OperatorNot, operands=operands)
        root.set_index(self._index)
        actual = root.get_postings()
        expected = {2}
        self.assertEqual(expected, actual)

    def test_BooleanQuery_Not_all_docs(self):
        '''Testing query results for "!algebrafsqffsqfic"'''
        operands = [WordLeaf("algebrafsqffsqfic")]
        root = OperatorNode(operator=OperatorNot, operands=operands)
        root.set_index(self._index)
        actual = root.get_postings()
        expected = {1, 2}
        self.assertEqual(expected, actual)

    def test_BooleanQuery_AllOperators(self):
        '''Testing query results for "(algrebraic + extraction) * !algebraic"'''
        operands1 = [WordLeaf("algebraic"), WordLeaf("extraction")]
        operator1 = OperatorNode(operator=OperatorOr, operands=operands1)
        operands2 = [WordLeaf("algebraic")]
        operator2 = OperatorNode(operator=OperatorNot, operands=operands2)
        operands3 = [operator1, operator2]
        root = OperatorNode(operator=OperatorAnd, operands=operands3)
        root.set_index(self._index)
        actual = root.get_postings()
        expected = {2}
        self.assertEqual(expected, actual)
