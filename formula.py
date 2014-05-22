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

        elif proof_term.token() == '*': # if_mult
            print(indent + ' operation type is "*"')
            print(indent + ' \tleft is: ' + str(proof_term.left()))
            print(indent + ' \tright is: ' + str(proof_term.right()))

            if proof_term.left().is_leaf():
                matches = Formula.match_for_implication(cs[str(proof_term.left())], str(subformula))
                print(indent + ' \tmatches for X in cs s.t. '+str(proof_term.left())+':(X->'+str(subformula) + '): \t' + str(matches))
                if proof_term.right().is_leaf():
                    for formula in matches:
                        if formula in cs[str(proof_term.right())]:
                            print(indent + ' \talso matches for X in cs s.t. ' + str(proof_term.right())+':X: \tTrue!')
                            return True
                    return False
                else:
                    for formula in matches:
                        print(indent + ' \tnew formula: (' + str(proof_term.right()) + ':' + formula + ')')
                        new_formula = Formula('(' + str(proof_term.right()) + ':' + formula + ')')
                        if new_formula.is_provable(cs):
                            return True
                    return False
            else:
                #todo
                return False



    def proof_term(self):
        return self._tree.left().subtree()

    def subformula(self):
        return self._tree.right().subtree()

    def is_axiom(self, cs):
        proof_term = self.proof_term().token()
        subformula = self.subformula().token()
        return subformula in cs[proof_term]

    @staticmethod
    def match_for_implication(maybes, subformula):
        imp = []
        for item in maybes:
            tree = Node.make_tree(item)
            if tree.token() == '->' and str(tree.right()) == subformula:
                imp.append(str(tree.left()))
        return imp

