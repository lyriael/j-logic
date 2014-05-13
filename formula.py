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

    def is_provable(self, cs, indent=''):
        proof_term = self.proof_term()
        subformula = self.subformula()
        print(indent + ' is ' + str(self) + ' provable?')
        print(indent + ' \tProof term: ' + str(proof_term) + ',\t token: ' + proof_term.token())
        print(indent + ' \tSubformula: ' + str(subformula) + ',\t token: ' + subformula.token())

        if proof_term.is_leaf():  # if_constant
            print(indent + ' operation type is "constant"')
            print(indent + ' \t"'+str(proof_term)+' => ' + str(subformula) + '" in cs? ')
            print(indent + ' \t' + str(self.is_axiom(cs)) + '!')
            print('')
            return self.is_axiom(cs)
        elif proof_term.token() == '!':  # if_bang
            print(indent + ' operation type is "!"')
            print(indent + ' \tProof term and subformula have same constant?')
            new_formula = Formula(str(subformula))

            if proof_term.inorder()[1:] == new_formula.proof_term().inorder():
                print(indent + ' \tTrue!')
                indent += ' -->'
                print('')
                return new_formula.is_provable(cs, indent)
            else:
                print(indent + ' \tFalse!')
                print('')
                return False
        elif proof_term.token() == '+':  # if_sum
            print(indent + ' operation type is "+"')
            print(indent + ' \tleft: (' + str(proof_term.left()) + ":" + str(subformula) + ')')
            print(indent + ' \tright: (' + str(proof_term.right()) + ":" + str(subformula) + ')')
            print('')
            indent += ' -->'
            left_formula = Formula('(' + str(proof_term.left()) + ":" + str(subformula) + ')')
            right_formula = Formula('(' + str(proof_term.right()) + ":" + str(subformula) + ')')
            return left_formula.is_provable(cs, indent) or right_formula.is_provable(cs, indent)

    def proof_term(self):
        return self._tree.left().subtree()

    def subformula(self):
        return self._tree.right().subtree()

    def is_axiom(self, cs):
        proof_term = self.proof_term().token()
        subformula = self.subformula().token()
        return cs[proof_term] == subformula


