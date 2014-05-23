from formula import Formula


class ProofSearch:

    def __init__(self, formula, cs):
        '''
        expect a string as formula
        '''
        self._formula = Formula(formula)
        self._cs = cs

    def find_in_cs(self, proof_term, subformula):
        operation = proof_term.operation()
        if operation == '':
            return subformula in self._cs[proof_term]
        elif proof_term.operation() == '+':
            self.resolve_plus(proof_term, subformula)
        elif proof_term.operation == '!':
            return 'blubb'


    def resolve_plus(self, proof_term, subformula):
        self.find_in_cs(proof_term.left(), subformula)
        self.find_in_cs(proof_term.right(), subformula)


