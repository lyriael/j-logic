from formula import Formula
from tree import Tree


class ProofSearch:

    def __init__(self, cs, formula):
        '''
        expect a string as formula
        '''
        self._cs = cs
        self._formula = Formula(formula)

    def divide(self):
        # of those tiny-formulas it is enough to prove just one
        big_mama = {}
        for small in self._formula.to_pieces():
            # find how that structre looks in test_formula#test_to_pieces_and_get_terms_to_proof
            big_mama[small.formula] = small.get_terms_to_proof()
        return big_mama

    def conquer(self, smalls):
        '''
        small: list of tuples
        e.g.
        [('a','F'), ('a', 'X1'), ('b', '(X2->F)']
        all those tuples must be found in cs.
        '''
        wilds = {}


