__author__ = 'lyriael'
from tree_node import Node

class Formula:

    def __init__(self, expression):
        root = Node.make_tree(expression)[0]
        assert str(root) == ':'

        self.proof_term = root.left()
        self.subformula = root.right()

    def __repr__(self):
        return self.proof_term.inorder() + ":" + self.subformula.inorder()

    def expression(self):
        return str(self)


    # Main method of class Formula. Evaluates if a Formula is provable.
    def is_provable(self, cs):

        # e.g. t: A
        if self.proof_term.is_constant():
            return "todo"
        # e.g. (t+s): A
        elif self.proof_term.is_sum():
            left = Formula(self.proof_term.left() + ":" + str(self.subformula))
            right = Formula(self.proof_term.right() + ":" + str(self.subformula))
            return left.is_provable(cs) or right.is_provable(cs)
        # e.g. !t:(t: A)
        elif proof_term.is_bang():
            new_formula = Formula(self.subformula)
            if self.proof_term.remove_bang() == new_formula.proof_term:
                return new_formula.is_provable(cs)
            else:
                return False
        return False

    def is_axiom(self, proof_term, cs):
        return cs[proof_term] == self.get_subformula
