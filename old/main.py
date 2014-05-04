# Formula consists of a proof term and a subformula. The subformula can also contain
# a proof term, but eventually the subformula should be derived from the Axioms.
# As for now, the allowed axioms are: -> (implication), ¬ (not)
# the allowed proof terms are: + (sum/union), ! (bang)

from old import parser


class Formula:

    expression = None

    def __init__(self, expression):
        self.expression = expression
        self.subformula = self.get_subformula(expression)

    # Main method of class Formula. Evaluates if a Formula is provable.
    def is_provable(self, cs):

        proof_term = self.get_proof_term()
        # e.g. t: A
        if proof_term.is_constant():
            return self.is_axiom(proof_term, cs)
        # e.g. (t+s): A
        elif proof_term.is_sum():

            left = Formula(self.proof_term.left(), self.subformula)
            right = Formula(self.proof_term.right(), self.subformula)
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

    def get_proof_term(self):
        #todo TEST
        colon = parser.find_right_most_colon(self.expression)
        return parser.clean_braces(self.expression[colon:])

    def get_subformula(self):
        #todo TEST
        colon = parser.find_right_most_colon(self.expression)
        return parser.clean_braces(self.expression[:colon])

    def get_representation(self):
        return

class ProofTerm():
    _types = ['CONSTANT', 'SUM', 'BANG']

    def __init__(self, expression, type=None):
        self.expression = expression
        self.type = type

    #TODO for all of those!!
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
        return
    # 'private' functions. Seams like that doesn't really exists in python, only the convention to use an underscore.


