from formula import Formula
from helper import parse

class ProofSearch:

    def __init__(self, formula, cs):
        '''
        expect a string as formula
        '''
        self._formula = Formula(formula)
        self._cs = cs
        self._proof = []

    def find_in_cs(self, proof_term, subformula):
        operation = proof_term.top_operation()
        if operation is None:
            if str(subformula) in self._cs[str(proof_term)]:
                self._proof.append(proof_term.to_s()+':'+subformula.to_s())
        elif operation == '+':
            self.resolve_plus(proof_term, subformula)
        elif operation == '!':
            self.resolve_bang(proof_term, subformula)
        elif operation == '*':
            self.resolve_mult(proof_term, subformula)
        return self._proof

    def resolve_plus(self, proof_term, subformula):
        self.find_in_cs(proof_term.left_operand(), subformula)
        self.find_in_cs(proof_term.right_operand(), subformula)

    def resolve_bang(self, proof_term, subformula):
        if subformula.top_operation() == ':' and proof_term.right_operand().to_s() is subformula.left_operand().to_s():
            self.find_in_cs(subformula.left_operand(), subformula.right_operand())

    def resolve_mult(self, proof_term, subformula):
        left = proof_term.left_operand()
        right = proof_term.right_operand()
        if left.is_const() and right.is_const():
            candidates = self.find_candidates_left(str(left), subformula)
            matches = self.check_candidates_right(str(right), candidates)
            for match in matches:
                self.find_in_cs(left, Formula('(' + match + '->' + str(subformula) + ')'))
                self.find_in_cs(right, Formula(match))

    def find_candidates_left(self, key, subformula):
        candidates = []
        for term in self._cs[key]:
            f = Formula(term)
            if f.top_operation() == '->' and str(f.right_operand()) == str(subformula):
                candidates.append(str(f.left_operand()))
        return candidates

    def check_candidates_right(self, key, candidates):
        matches = []
        for candidate in candidates:
            for term in self._cs[key]:
                if term == candidate:
                    matches.append(term)
        return matches