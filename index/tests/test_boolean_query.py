import unittest
import os
from index.boolean_query import OperatorNot, OperatorAnd, OperatorOr, OperatorNode, WordLeaf
from index.index import Index
from index.index_config import IndexConfig

class BooleanQueryTests(unittest.TestCase):
    def setUp(self):
        WordLeaf._index = Index(os.path.dirname(os.path.realpath(__file__)) + "/test_data", IndexConfig())

    def test_BooleanQuery_Or_simple(self):
        '''Test "algrebraic + extraction"'''
        operands = [WordLeaf("algebraic"), WordLeaf("extraction")]
        root = OperatorNode(operator = OperatorOr, operands = operands)
        actual = root.getPostings()
        expected = {1, 2}
        self.assertEqual(expected, actual)

    def test_BooleanQuery_Or_redundancy(self):
        '''Test "language + extraction"'''
        operands = [WordLeaf("language"), WordLeaf("extraction")]
        root = OperatorNode(operator = OperatorOr, operands = operands)
        actual = root.getPostings()
        expected = {1, 2}
        self.assertEqual(expected, actual)

    def test_BooleanQuery_And_simple(self):
        '''Test "algrebraic * extraction"'''
        operands = [WordLeaf("algebraic"), WordLeaf("extraction")]
        root = OperatorNode(operator = OperatorAnd, operands = operands)
        actual = root.getPostings()
        expected = set()
        self.assertEqual(expected, actual)

    def test_BooleanQuery_And_no_results(self):
        '''Test "language * extraction"'''
        operands = [WordLeaf("language"), WordLeaf("extraction")]
        root = OperatorNode(operator = OperatorAnd, operands = operands)
        actual = root.getPostings()
        expected = {2}
        self.assertEqual(expected, actual)

    def test_BooleanQuery_Not_simple(self):
        '''Test "!algebraic"'''
        operands = [WordLeaf("algebraic")]
        root = OperatorNode(operator = OperatorNot, operands = operands)
        actual = root.getPostings()
        expected = {2}
        self.assertEqual(expected, actual)

    def test_BooleanQuery_Not_all_docs(self):
        '''Test "!algebrafsqffsqfic"'''
        operands = [WordLeaf("algebrafsqffsqfic")]
        root = OperatorNode(operator = OperatorNot, operands = operands)
        actual = root.getPostings()
        expected = {1, 2}
        self.assertEqual(expected, actual)

    def test_BooleanQuery_AllOperators(self):
        '''Test "(algrebraic + extraction) * !algebraic"'''
        operands1 = [WordLeaf("algebraic"), WordLeaf("extraction")]
        operator1 = OperatorNode(operator = OperatorOr, operands = operands1)
        operands2 = [WordLeaf("algebraic")]
        operator2 = OperatorNode(operator = OperatorNot, operands = operands2)
        operands3 = [operator1, operator2]
        root = OperatorNode(operator = OperatorAnd, operands = operands3)
        actual = root.getPostings()
        expected = {2}
        self.assertEqual(expected, actual)
