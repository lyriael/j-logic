__author__ = 'lyriael'
#aka tree
from tree_node import Node


class Formula(object):

    def __init__(self, formula):
        '''
        string as formula expected. Be careful to put all parentheses.
        '''
        if isinstance(formula, str):
            self._tree = Node.make_tree(formula)
        elif isinstance(formula, Node):
            self._tree = formula.deep_copy()
        elif isinstance(formula, Formula):
            self._tree = formula.tree()
        self._op = self._tree.token()
        if self._tree.has_left():
            self._left = str(self._tree.left())
        if self._tree.has_right():
            self._right = str(self._tree.right())

    def __str__(self):
        return str(self._tree)

    def to_s(self):
        return str(self)

    def proof_term(self):
        if self._op == ':':
            return Formula(self._left)
        raise Exception('Has no proof_term')

    def subformula(self):
        if self._op == ':':
            return Formula(self._right)
        raise Exception('Has no subformula')

    def top_operation(self):
        if self._tree.token() in ['+', '*', '!', ':', '->']:
            return self._tree.token()

    def left_operand(self):
        if self._tree.token() in ['+', '*', '->', ':']:
            return Formula(self._tree.left())

    def right_operand(self):
        if self._tree.token() in ['+', '*', '->', ':', '!']:
            return Formula(self._tree.right())

    def is_const(self):
        return len(self._tree) == 1

    def tree(self):
        '''
        returns a deep copy of tree
        '''
        return self._tree.deep_copy()


    @staticmethod
    def from_parts(proof_term, subformula):
        '''
        returns a new formula, using deep copy.
        '''
        return Formula('('+str(proof_term)+':'+str(subformula)+')')

    @staticmethod
    def match_for_implication(maybes, subformula):
        imp = []
        for item in maybes:
            tree = Node.make_tree(item)
            if tree.token() == '->' and str(tree.right()) == subformula:
                imp.append(str(tree.left()))
        return imp

