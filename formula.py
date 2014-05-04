__author__ = 'lyriael'
#aka tree
from tree_node import Node


class Formula(object):

    def __init__(self, formula):

        if isinstance(formula, str):
            self._tree = Node.make_tree(formula)
        elif isinstance(formula, Node):
            self._tree = formula

    def __str__(self):
        return str(self._tree)

    def is_provable(self, cs):
        proof_term = self.proof_term()
        subformula = self.subformula()
        print('-------------------------')
        print('is provable? ' + str(self))
        print('--> Proof term: ' + str(proof_term) + ',\t token: ' + proof_term.token())
        print('--> Subformula: ' + str(subformula) + ',\t token: ' + subformula.token())

        if proof_term.is_leaf():  # if_constant
            print('--> --> is leaf')
            return self.is_axiom(cs)
        elif proof_term.token() == '!':  # if_bang
            print('--> --> is bang')
            print('--> --> --> ' + str(subformula))
            new_formula = Formula(str(subformula))
            if proof_term.inorder()[1:] == new_formula.proof_term().inorder():
                return new_formula.is_provable(cs)
            else:
                return False
        elif proof_term.token() == '+':  # if_sum
            print('--> --> is sum')
            print('--> --> --> left: (' + str(proof_term.left()) + ":" + str(subformula) + ')')
            print('--> --> --> right: (' + str(proof_term.right()) + ":" + str(subformula) + ')')
            left_formula = Formula('(' + str(proof_term.left()) + ":" + str(subformula) + ')')
            right_formula = Formula('(' + str(proof_term.right()) + ":" + str(subformula) + ')')
            return left_formula.is_provable(cs) or right_formula.is_provable(cs)

    def proof_term(self):
        return self._tree.left().subtree()

    def subformula(self):
        return self._tree.right().subtree()

    def is_axiom(self, cs):
        #debug stuff
        print('----is axiom?----')
        print('--> proof term: ' + self.proof_term().token())
        print('--> subformula: ' + self.subformula().token())
        print('--> cs: ' + str(cs))
        print('--> --> ' + str(cs[str(self.proof_term())] == str(self.subformula())))
        proof_term = self.proof_term().token()
        subformula = self.subformula().token()
        return cs[proof_term] == subformula


