import re

class OperatorOr:
    @staticmethod
    def applyOperator(operands):
        return { posting for op in operands for posting in op.getPostings() }

class OperatorAnd:
    @staticmethod
    def applyOperator(operands):
        all_postings = set()
        for (idx, op) in enumerate(operands):
            postings = op.getPostings()
            if idx > 0:
                all_postings = all_postings.intersection(set(postings))
            else:
                all_postings = set(postings)
        return all_postings

class OperatorNot:
    @staticmethod
    def applyOperator(operands):
        if len(operands) != 1:
            raise ValueError("The NOT operator should be used with exactly one operand")
        all_docs = set(WordLeaf._index.getAllDocIds())
        return all_docs.difference(operands[0].getPostings())

class BooleanExpressionParser:
    def __init__(self):
        self._binary_operators = {
            '+': OperatorOr,
            '*': OperatorAnd
        }
        self._unary_operators = {
            '!': OperatorNot
        }
        self._initPatterns()

    def parseExpression(self, expression):
        '''Recursively constructs an evaluation tree for a boolean query.'''
        binary_expr = self._parseBinaryExpression(expression)
        if binary_expr:
            return binary_expr

        unary_expr = self._parseUnaryExpression(expression)
        if unary_expr:
            return unary_expr

        single_operand = self._parseSingleOperand(expression)
        if single_operand:
            return single_operand

        raise ValueError("Invalid boolean query: <" + expression + ">.")

    def _initPatterns(self):
        binary_operator_pattern = r'[{0}]'.format("".join(self._binary_operators.keys()))
        unary_operator_pattern = r'[{0}]'.format("".join(self._unary_operators.keys()))
        operand_pattern = r'\(?[\(\)\w{0}{1}]+\)?'.format("".join(self._unary_operators.keys()), "".join(self._binary_operators.keys()))

        unary_expr_pattern_format = r'^\s*(?P<operator>{0})\s*(?P<operand>{1})\s*$'
        binary_expr_pattern_format = r'^\s*(?P<operand1>{0})\s*(?P<operator>{1})\s*(?P<operand2>{2})\s*$'

        self._single_operand_pattern = r'^\s*(?P<operand>{0})\s*$'.format(operand_pattern)
        self._unary_expr_pattern = unary_expr_pattern_format.format(unary_operator_pattern, operand_pattern)
        self._binary_expr_pattern = binary_expr_pattern_format.format(operand_pattern, binary_operator_pattern, operand_pattern)

    def _parseBinaryExpression(self, expression):
        matches = re.match(self._binary_expr_pattern, expression)
        if matches:
            operand1 = self.parseExpression(matches.group('operand1'))
            operand2 = self.parseExpression(matches.group('operand2'))
            operator = self._binary_operators[matches.group('operator')]
            return OperatorNode(operator, [operand1, operand2])

    def _parseUnaryExpression(self, expression):
        matches = re.match(self._unary_expr_pattern, expression)
        if matches:
            operand = self.parseExpression(matches.group('operand'))
            operator = self._unary_operators[matches.group('operator')]
            return OperatorNode(operator, [operand])

    def _parseSingleOperand(self, expression):
        matches = re.match(self._single_operand_pattern, expression)
        if matches:
            operand = matches.group('operand')
            return WordLeaf(operand)


class BooleanQuery:
    '''Represents a boolean query that can use the * (and), + (or) and ! (not) operators'''
    def __init__(self, query, parser = BooleanExpressionParser()):
        self._root = parser.parseExpression(query)

    def execute(self):
        if self._root:
            return self._root.getPostings()
        else:
            raise ValueError("There is no valid boolean query to execute.")

class OperatorNode:
    '''Node in the boolean query execution tree'''
    def __init__(self, operator = "", operands = []):
        self._operator = operator
        self._operands = operands

    def __str__(self):
        return '{operator: ' + str(self._operator) + ', operands: [' + ', '.join([str(operand) for operand in self._operands]) + ']}'

    def __unicode__(self):
        return unicode(str(self))

    def getPostings(self):
        return self._operator.applyOperator(self._operands)

class WordLeaf:
    '''Leaf in the boolean query execution tree'''
    _index = None

    def __init__(self, word):
        self._index
        self._word = word

    def __str__(self):
        return self._word

    def __unicode__(self):
        return unicode(str(self))

    def getPostings(self):
        return { posting['docId'] for posting in self._index.search(self._word) }
