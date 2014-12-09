import unittest
from index.boolean_query import *

class BooleanQueryParserTests(unittest.TestCase):
    def test_BooleanQueryParser_simple_expression(self):
        expression = "algebraic + language"
        operands = [WordLeaf('algebraic'), WordLeaf('language')]
        expected_root = OperatorNode(OperatorOr, operands)
        actual_root = BooleanQuery(expression)._root
        self.assertEqual(str(expected_root), str(actual_root))

    def test_BooleanQueryParser_unary_operator(self):
        expression = "!algebraic"
        operands = [WordLeaf('algebraic')]
        expected_root = OperatorNode(OperatorNot, operands)
        actual_root = BooleanQuery(expression)._root
        self.assertEqual(str(expected_root), str(actual_root))
