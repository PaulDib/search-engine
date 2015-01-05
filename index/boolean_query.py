'''
Provides classes to create and execute a boolean query on an index.
'''
import re
from pyparsing import nestedExpr


class AbstractOperator(object):

    ''' Boolean operator base class.'''

    def __init__(self):
        pass

    @staticmethod
    def apply_operator(operands):
        ''' Apply the operator to the input operands. '''
        pass


class OperatorOr(AbstractOperator):

    '''
    Or operator.
    '''
    @staticmethod
    def apply_operator(operands):
        return {posting for op in operands for posting in op.get_postings()}


class OperatorAnd(AbstractOperator):

    '''
    And operator.
    '''
    @staticmethod
    def apply_operator(operands):
        all_postings = set()
        for (idx, operand) in enumerate(operands):
            postings = operand.get_postings()
            if idx > 0:
                all_postings = all_postings.intersection(set(postings))
            else:
                all_postings = set(postings)
        return all_postings


class OperatorNot(AbstractOperator):

    '''
    Not operator.
    '''
    @staticmethod
    def apply_operator(operands):
        if len(operands) != 1:
            raise ValueError("The NOT operator should be \
                used with exactly one operand")
        all_docs = set(operands[0]._index.get_all_doc_ids())
        return all_docs.difference(operands[0].get_postings())


class OperatorNode(object):

    '''Node in the boolean query execution tree'''

    def __init__(self, operator=None, operands=None):
        if operands is None:
            self._operands = []
        else:
            self._operands = operands
        self._operator = operator

    def __str__(self):
        return ('{operator: ' + str(self._operator) + ', operands: ['
                + ', '.join([str(operand) for operand in self._operands])
                + ']}')

    def __unicode__(self):
        return unicode(str(self))

    def get_postings(self):
        '''Returns the result of apply the operator node.'''
        return self._operator.apply_operator(self._operands)

    def add_operand(self, operand):
        '''Add an operand to the operator.'''
        self._operands.append(operand)

    def set_index(self, index):
        '''Recursively sets the index for the node and its children.'''
        for operand in self._operands:
            operand.set_index(index)


class WordLeaf(object):

    '''Leaf in the boolean query execution tree'''

    def __init__(self, word):
        self._index = None
        self._word = word

    def __str__(self):
        return self._word

    def __unicode__(self):
        return unicode(str(self))

    def get_postings(self):
        '''Returns the result of apply the operator node.'''
        return {posting['doc_id'] for posting in self._index.search(self._word)}

    def set_index(self, index):
        '''Recursively sets the index for the node and its children.'''
        self._index = index


class BooleanExpressionParser(object):

    '''
    Parses a boolean expression and creates the execution tree.
    '''

    def __init__(self):
        self._binary_operators = {
            '+': OperatorOr,
            '*': OperatorAnd
        }
        self._unary_operators = {
            '!': OperatorNot
        }

    def parse_expression(self, expression):
        '''
        Constructs an evaluation tree for a boolean query.
        Returns the root of the tree.
        '''
        expression = self.format_expression(expression)
        try:
            nested = nestedExpr().parseString(expression).asList()
            return self._create_operator(nested)
        except:
            raise ValueError("Parsing failed")

    def format_expression(self, expression):
        '''
        Formats an expression by removing whitespace.
        '''
        expression = '(' + re.sub(r'[\s]', '', expression) + ')'
        op_pattern = r'([{0}{1}])'.format(
            "".join(self._binary_operators.keys()),
            "".join(self._unary_operators.keys()))
        expression = re.sub(op_pattern, r" \1 ", expression)
        return expression

    def _create_operator(self, nested_item):
        '''
        Returns the root operator corresponding to a list of words,
        operators, and nested expressions.
        '''
        if isinstance(nested_item, str):
            is_operator = nested_item in self._binary_operators
            is_operator = is_operator or nested_item in self._unary_operators
            if is_operator:
                return nested_item
            else:
                return WordLeaf(nested_item)
        if isinstance(nested_item, list):
            operators = [self._create_operator(item) for item in nested_item]
            return self._combine_operators(operators)
        raise ValueError("Parsing failed.")

    def _combine_operators(self, operators):
        '''Returns the operator corresponding to a list of operators.'''
        if not operators:
            raise ValueError("Invalid expression")

        combined = self._combine_unary_operators(operators)
        return self._combine_binary_operators(combined)

    def _combine_unary_operators(self, operators):
        '''
        Returns the node corresponding to the applied unary operator.
        '''
        combined_ops = []
        is_operand = False
        last_operator = None
        node = None
        for i in range(0, len(operators)):
            operator = operators[i]
            if operator in self._unary_operators:
                if i + 1 >= len(operators):
                    raise ValueError("Unary operator should \
                        be followed by its operand.")
                node = OperatorNode(self._unary_operators[operator])
                if is_operand:
                    combined_ops[i - 1].add_operand(node)
                else:
                    is_operand = True
                    combined_ops.append(node)
                last_operator = node
            elif is_operand:
                last_operator.add_operand(operator)
                is_operand = False
            else:
                combined_ops.append(operator)
        return combined_ops

    def _combine_binary_operators(self, operators):
        '''
        Returns the node corresponding to the applied binary operator.
        '''
        root = operators[0]
        for i in range(1, len(operators)):
            operator = operators[i]
            if operator in self._binary_operators:
                if i - 1 < 0 or i + 1 >= len(operators):
                    raise ValueError("Binary operator should \
                        be between its operands.")
                root = OperatorNode(
                    operator=self._binary_operators[operator],
                    operands=[root])
            else:
                root.add_operand(operator)
        return root


class BooleanQuery(object):

    '''
    Represents a boolean query.
    The query can use the * (and), + (or) and ! (not) operators.
    '''

    def __init__(self, query, parser=BooleanExpressionParser()):
        self._root = parser.parse_expression(query)

    def execute(self, index=None):
        '''Executes the query and returns the postings.'''
        if index:
            self.set_index(index)
        if self._root:
            return self._root.get_postings()
        else:
            raise ValueError("There is no valid boolean query to execute.")

    def set_index(self, index):
        '''Set the index used for the query.'''
        self._root.set_index(index)
