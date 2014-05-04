__author__ = 'lyriael'
#aka tree
from tree_node import Node


class Formula(object):

    def __init__(self, formula):

        if isinstance(formula, str):
            self.tree_rep = Node.make_tree(formula)
        elif isinstance(formula, Node):
            self.tree_rep = formula

        # assert self.tree_rep.token == ':'
        # assert self.tree_rep.has_right() and self.tree_rep.has_left()

    def is_provable(self, cs):
        print(self)
        proof_term = self.proof_term()
        subformula = self.subformula()

        if proof_term.is_leaf():  # if_constant
            return self.is_axiom(cs)
        elif proof_term.token == '!':  # if_bang
            new_formula = Formula(subformula)
            if proof_term.inorder()[1:] == new_formula.proof_term().inorder():
                return new_formula.is_provable(cs)
            else:
                return False
        elif proof_term.token == '+':  # if_sum
            left_formula = Formula(proof_term.get_left().inorder() + ":" + subformula.inorder())
            right_formula = Formula(proof_term.get_right().inorder() + ":" + subformula.inorder())
            return left_formula.is_provable(cs) or right_formula.is_provable(cs)

    def proof_term(self):
        return self.tree_rep.get_left()

    def subformula(self):
        return self.tree_rep.get_right()

    def is_axiom(self, cs):
        return cs[self.proof_term()] == self.subformula()

    def __str__(self):
        return self.tree_rep.inorder()

# Tests

# Test if formula may be instanciated as string as well as a node
a = Formula('(a+b)')
n = Node()
n.token = 'a'
b = Formula(n)
print(b.tree_rep.inorder())

cs = {'a': 'A', 'b': 'B', 'c': 'C'}
f = Formula('((a+b):B)')
print(f)
print(f.is_provable(cs))
