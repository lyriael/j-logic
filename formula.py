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
        #not sure if this part is used.... its a bit confusing...
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
        '''
        returns the root token of the formula tree if it is a operation (ink. '->'),
        and 'const' if it is a constant and therefore a leaf.
        '''
        if self._tree.token() in ['+', '*', '!', ':', '->']:
            return self._tree.token()
        else:
            return 'const'

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

    def is_in(self, cs):
        subformula = str(self.subformula())
        proof_term = str(self.proof_term())
        if (proof_term in cs) and subformula in cs[proof_term]:
            return True
        else:
            False

    def split(self):
        '''
        Returns an array with formulas, where each formula represents an operand of '+'
        '''
        parts = []
        if self.proof_term().top_operation() == '+':
            left = Formula.parts_to_formula(self.proof_term().left_operand(), self.subformula())
            right = Formula.parts_to_formula(self.proof_term().right_operand(), self.subformula())
            parts = parts + left.split() + right.split()
        else:
            parts = [str(self.proof_term())]
        return parts

    def _remove_bangs(self):
        '''
        This method is intended only for left subtrees of '*'.
        It will remove all Nodes, that have '!' as token.
        '''
        self._tree.remove_bangs()

    def collect(self):
        '''
        This method is just a bridge between ProofSearch and TreeNode.
        '''
        nodes = self._tree.collect_nodes(self._tree)
        formulas = []
        for node in nodes:
            formulas.append(Formula(node))
        return formulas

    @staticmethod
    def parts_to_formula(proof_term, subformula):
        '''
        returns a new formula, using deep copy.
        '''
        return Formula('('+str(proof_term)+':'+str(subformula)+')')

    @staticmethod
    def parts_to_s(proof_term, subformula):
        '''
        returns string of combination from proof_term and subformula.
        '''
        return '('+str(proof_term)+':'+str(subformula)+')'

    @staticmethod
    def match_for_implication(maybes, subformula):
        imp = []
        for item in maybes:
            tree = Node.make_tree(item)
            if tree.token() == '->' and str(tree.right()) == subformula:
                imp.append(str(tree.left()))
        return imp

