from formula import Formula
from helper import parse


class ProofSearch:

    def __init__(self, cs, formula):
        '''
        expect a string as formula
        '''
        self._cs = cs
        self._formula = Formula(formula)
        self._to_proof = {str(self._formula.subformula()): [str(self._formula.proof_term())]}

    def get_ready(self):
        self._to_proof[str(self._formula.subformula())] = self._formula.split()


    def is_provable(self):
        proof_term = self._formula.proof_term()
        subformula = self._formula.subformula()

        case = proof_term.top_operation()  # should be one of +, !, * or const

        if case == '+':
            left = self._formula.left_operand()

        if case == 'const' and self._formula.is_in(self._cs):
            return True
        else:
            return False

