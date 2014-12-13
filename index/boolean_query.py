import re
from pyparsing import nestedExpr

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

    def parseExpression(self, expression):
        '''Constructs an evaluation tree for a boolean query.'''
        expression = self.formatExpression(expression)
        nested = nestedExpr().parseString(expression).asList()
        return self._createOperator(nested)

    def _createOperator(self, nestedItem):
        '''Returns the root operator corresponding to a list of words, operators, and nested expressions.'''
        if isinstance(nestedItem, str):
            if nestedItem in self._binary_operators or nestedItem in self._unary_operators:
                return nestedItem
            else:
                return WordLeaf(nestedItem)
        if isinstance(nestedItem, list):
            operators = [self._createOperator(item) for item in nestedItem]
            return self._combineOperators(operators)
        raise ValueError("Parsing failed.")

    def _combineOperators(self, operators):
        '''Returns the operator corresponding to a list of operators.'''
        if not operators:
            raise ValueError("Invalid expression")

        root = self._combineUnaryOperators(operators)
        return root[0]

    def _combineUnaryOperators(self, operators):
        combined_ops = []
        is_operand = False
        last_operator = None
        node = None
        for i in range(0, len(operators)):
            op = operators[i]
            if op in self._unary_operators:
                if i + 1 >= len(operators):
                    raise ValueError("Unary operator should be followed by its operand.")
                node = OperatorNode(self._unary_operators[op])
                if is_operand:
                    combined_ops[i-1].addOperand(node)
                else:
                    is_operand = True
                    combined_ops.append(node)
                last_operator = node
            elif is_operand:
                last_operator.addOperand(op)
                is_operand = False
            else:
                combined_ops.append(op)
        return combined_ops

    def _combineBinaryOperators(self, operators):  
        combined_ops = []
        last_operator = operators[0]
        for i in range(1, len(operators)):
            op = operators[i]
            if op in self._binary_operators:
                if i - 1 < 0 or i + 1 >= len(operators):
                    raise ValueError("Binary operator should be between its operands.")
                last_operator = OperatorNode(operator = self._binary_operators[op], operands = [last_operator])
            else:
                last_operator.addOperand(op)
        return last_operator

    def formatExpression(self, expression):
        expression = '(' + re.sub('[\s]', '', expression) + ')'
        op_pattern = r'([{0}{1}])'.format("".join(self._binary_operators.keys()), "".join(self._unary_operators.keys()))
        expression = re.sub(op_pattern, r" \1 ", expression)
        return expression

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
    def __init__(self, operator = None, operands = []):
        self._operator = operator
        self._operands = operands

    def __str__(self):
        return '{operator: ' + str(self._operator) + ', operands: [' + ', '.join([str(operand) for operand in self._operands]) + ']}'

    def __unicode__(self):
        return unicode(str(self))

    def getPostings(self):
        return self._operator.applyOperator(self._operands)

    def addOperand(self, operand):
        self._operands.append(operand)

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
