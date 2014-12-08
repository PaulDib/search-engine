class BooleanQueryParser:
    def __init__(self, query):
        pass

class OperatorNode:
    def __init__(self, operator = "", operands = []):
        self._operator = operator
        self._operands = operands

    def getPostings(self):
        return self._operator.applyOperator(self._operands)

class WordLeaf:
    _index = None

    def __init__(self, word):
        self._index
        self._word = word

    def getPostings(self):
        return { posting['docId'] for posting in self._index.search(self._word) }

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
