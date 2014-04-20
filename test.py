# Formula consists of a proof term and a subformula. The subformula can also contain
# a proof term, but eventually the subformula should derived from the Axioms.
# As for now, the allowed axioms are: -> (implication), ¬ (not)
# the allowed proof terms are: + (sum/union), ! (bang)


class Formula:

    is_axiom = False     # is_leaf

    def __init__(self, c, A):
        self.proof_term = c
        self.subformula = A

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


class ProofTerm:

    def __init__(self, t):
        self.term = t

    def is_constant(self):
        #todo
        return True

    def is_sum(self):
        #todo
        return True

    def is_bang(self):
        #todo
        return True

    def get_left(self):
        #todo
        return False

    def get_right(self):
        #todo
        return False

    def remove_bang(self):
        #todo
        return self

## Helper class to parse String to


class Reader:

    formulas = ["atomic", "implication", "negation"]
    proof_terms = ["atomic", "sum", "bang"]

    @staticmethod
    def split(formula):
        #todo
        return formula


cs = {"c1": "¬A", "c2": "A->B"}
t = Formula("(!f)", "A->B")
print(t.to_String())