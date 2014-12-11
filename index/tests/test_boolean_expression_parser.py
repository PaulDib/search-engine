import unittest
from index.boolean_query import *

class BooleanExpressionParserTests(unittest.TestCase):
    def test_BooleanExpressionParser_simple_expression(self):
        expression = "algebraic + language"
        operands = [WordLeaf('algebraic'), WordLeaf('language')]
        expected_root = OperatorNode(OperatorOr, operands)
        actual_root = BooleanQuery(expression)._root
        self.assertEqual(str(expected_root), str(actual_root))

    def test_BooleanExpressionParser_unary_operator(self):
        expression = "!algebraic"
        operands = [WordLeaf('algebraic')]
        expected_root = OperatorNode(OperatorNot, operands)
        actual_root = BooleanQuery(expression)._root
        self.assertEqual(str(expected_root), str(actual_root))

    def test_BooleanExpressionParser_nested_expression(self):
        expression = "(algebraic*!language)+expression"
        opNot = OperatorNode(OperatorNot, [WordLeaf('language')])

        operands1 = [WordLeaf('algebraic'), opNot]
        operator1 = OperatorNode(OperatorAnd, operands1)

        operands2 = [operator1, WordLeaf('expression')]
        expected_root = OperatorNode(OperatorOr, operands2)

        actual_root = BooleanQuery(expression)._root
        self.assertEqual(str(expected_root), str(actual_root))
