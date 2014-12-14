import unittest
from index.boolean_query import *

class BooleanExpressionParserTests(unittest.TestCase):
    def test_BooleanExpressionParser_format_expression(self):
        '''Testing expression formatter'''
        expression = "algebraic+! language"
        formatted_expr = "(algebraic +  ! language)"
        parser = BooleanExpressionParser()
        self.assertEqual(formatted_expr, parser.formatExpression(expression))

    def test_BooleanExpressionParser_binary_operator(self):
        '''Testing query parsing for binary operator'''
        expression = "algebraic + language"
        operands = [WordLeaf('algebraic'), WordLeaf('language')]
        expected_root = OperatorNode(OperatorOr, operands)
        actual_root = BooleanQuery(expression)._root
        self.assertEqual(str(expected_root), str(actual_root))

    def test_BooleanExpressionParser_unary_operator(self):
        '''Testing query parsing for unary operator.'''
        expression = "!algebraic"
        operands = [WordLeaf('algebraic')]
        expected_root = OperatorNode(OperatorNot, operands)
        actual_root = BooleanQuery(expression)._root
        self.assertEqual(str(expected_root), str(actual_root))

    def test_BooleanExpressionParser_nested_expression(self):
        '''Testing query parsing for nested expression.'''
        expression = "(algebraic*!language)+expression"
        opNot = OperatorNode(OperatorNot, [WordLeaf('language')])

        operands1 = [WordLeaf('algebraic'), opNot]
        operator1 = OperatorNode(OperatorAnd, operands1)

        operands2 = [operator1, WordLeaf('expression')]
        expected_root = OperatorNode(OperatorOr, operands2)

        actual_root = BooleanQuery(expression)._root
        self.assertEqual(str(expected_root), str(actual_root))

    def test_BooleanExpressionParser_complex_expression(self):
        '''Testing query parsing for highly nested expression.'''
        self.maxDiff = None
        expression = "((algebraic+!language)*!(expression + (algebraic*language)))"
        opNot = OperatorNode(OperatorNot, [WordLeaf('language')])

        operands1 = [WordLeaf('algebraic'), opNot]
        leftOpOr = OperatorNode(OperatorOr, operands1)

        nestedAnd = OperatorNode(OperatorAnd, [WordLeaf('algebraic'), WordLeaf('language')])
        nestedOr = OperatorNode(OperatorOr, [WordLeaf('expression'), nestedAnd])
        rightOpNot = OperatorNode(OperatorNot, [nestedOr])

        operands2 = [leftOpOr, rightOpNot]
        expected_root = OperatorNode(OperatorAnd, operands2)

        actual_root = BooleanQuery(expression)._root
        self.assertEqual(str(expected_root), str(actual_root))

    def test_BooleanExpressionParser_unbalanced_expression_inside(self):
        '''Testing query parsing should fail with an unbalanced expression.'''
        expression = "algebraic * (language + expression"
        self.assertRaises(ValueError, BooleanQuery, expression)

    def test_BooleanExpressionParser_unbalanced_expression_beginning(self):
        '''Testing query parsing should fail with an unbalanced expression.'''
        expression = "(algebraic * language + expression"
        self.assertRaises(ValueError, BooleanQuery, expression)
