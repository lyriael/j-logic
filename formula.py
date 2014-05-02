import parser
import proof_term

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

            left = Formula(self.proof_term.get_left(), self.subformula)
            right = Formula(self.proof_term.get_right(), self.subformula)
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

    def get_subformula(self, expression):
        #todo TEST
        colon = parser.find_right_most_colon(self.expression)
        return parser.clean_braces(self.expression[:colon])

    def get_representation(self):
        return