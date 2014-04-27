# Formula consists of a proof term and a subformula. The subformula can also contain
# a proof term, but eventually the subformula should be derived from the Axioms.
# As for now, the allowed axioms are: -> (implication), ¬ (not)
# the allowed proof terms are: + (sum/union), ! (bang)

import sympy


class Formula:

    is_axiom = False     # is_leaf

    def __init__(self, a, c=None):
        self.subformula = a
        self.proof_term = c

    # Main method of class Formula. Evaluates if a Formula is provable.
    def is_provable(self, cs):
        # e.g. t: A
        if self.proof_term.is_constant():
            return self.is_axiom_of_cs(cs)
        # e.g. (t+s): A
        elif self.proof_term.is_sum():
            left = Formula(self.proof_term.get_left(), self.subformula)
            right = Formula(self.proof_term.get_right(), self.subformula)
            return left.is_provable(cs) or right.is_provable(cs)
        # e.g. !t:(t: A)
        elif self.proof_term.is_bang():
            a = Reader.split(self.subformula)
            new_formula = Formula(a[0], a[1])
            if self.proof_term.remove_bang() == new_formula.proof_term:
                return new_formula.is_provable(cs)
            else:
                return False
        return False

    def is_axiom_of_cs(self, cs):
        return cs[self.proof_term] == self.subformula

    def proof_term_split(self, x):
        '''
        tries to split from the subformula a proof_term.
        if it works, it will reassign the found proof_term to the object and overwrite the subformula with
        the remaining part of the original subformula.
        '''

        #todo
        return []


class ProofTerm():
    _types = ['CONSTANT', 'SUM', 'BANG']

    def __init__(self, expression, type=None):
        self.expression = expression
        self.type = type

    def is_constant(self):
        return self.type == 'CONSTANT'

    def is_sum(self):
        return self.type == 'SUM'

    def is_bang(self):
        return self.type == 'BANG'

    def set_type(self):
        #todo: somehow find out what typ this is.
        self.type = self._types[0]
        return self._types[0]

    def get_left(self):
        assert self.type == 'SUM', "Cannot get left if Proof Term is not of type SUM."
        #todo: read left variable
        return False

    def get_right(self):
        assert self.type == 'SUM', "Cannot get right if Proof Term is not of type SUM."
        #todo: read right variable
        return False

    def remove_bang(self):
        assert self.type == 'BANG', "Cannot remove BANG if Proof Term is not of type Bang."
        #todo: read inner
        return self

    @staticmethod
    def find_pt(expression):
        #todo: search through the string in order to finde the proof_term. If it exists, create a new ProofTerm.

    # 'private' functions. Seams like that doesn't really exists in python, only the convention to use an underscore.


