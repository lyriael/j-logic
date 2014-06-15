from formula import Formula
from helper import parse


class ProofSearch:

    def __init__(self, cs):
        '''
        expect a string as formula
        '''
        self._cs = cs
        self._proof = []
        self._counter = 0 #todo check what the cleanest solution for that is

    def find_in_cs(self, proof_term, subformula):
        '''
        looks up proof_term:subformula in cs, if for any constant proofterms s,t and any Formula F
        s:F, !s:F, (s+t):F or (s*t):F is the case and returns it as string.
        '''
        operation = proof_term.top_operation()
        if operation == 'const':
            if str(subformula) in self._cs[str(proof_term)]:
                self._proof.append(proof_term.to_s()+':'+subformula.to_s())
        else:
            left = proof_term.left_operand()
            right = proof_term.right_operand()
            if operation == '!':
                if right.is_const():
                    self.resolve_bang(proof_term, subformula)
            elif operation == '+':
                if left.is_const() and right.is_const():
                    self.resolve_plus(proof_term, subformula)
            elif operation == '*':
                if left.is_const() and right.is_const():
                    self.resolve_mult(proof_term, subformula)
        return self._proof

    def is_provable(self, proof_term, subformula, verbose=False):
        '''
        main function
        '''
        if verbose: print('is_provable: '+str(proof_term)+':'+str(subformula))
        case = proof_term.top_operation()
        if case == 'const':
            if verbose: print('looking for '+str(proof_term)+':'+str(subformula)+' in cs.')
            result = self.find_in_cs(proof_term, subformula)
            return result


    def resolve(self, proof_term, subformula, verbose=False):
        '''
        is_provable
        '''
        #todo tests!
        if verbose:
            print('resolve: '+proof_term.to_s+':'+subformula.to_s)
        if proof_term.top_operation() == '+':
            left = proof_term.left_operand()
            if left.is_const() and self.in_cs(left, subformula):
                self._proof.append(Formula.parts_to_s(left, subformula))
            else:
                self.resolve(left, subformula)
            right = proof_term.right_operand()
            if right.is_const() and self.in_cs(right, subformula):
                self._proof.append(Formula.parts_to_s(right, subformula))
            else:
                self.resolve(right, subformula)
            return'+'
        elif proof_term.top_operation() == '!':
            # if is left child, delete subtree
            return'!'
        elif proof_term.top_operation() == '*':
            # make a new variable, search for left term first, then right.
            return'*'

    def resolve_plus(self, proof_term, subformula):
        self.find_in_cs(proof_term.left_operand(), subformula)
        self.find_in_cs(proof_term.right_operand(), subformula)

    def resolve_bang(self, proof_term, subformula):
        if subformula.top_operation() == ':' and proof_term.right_operand().to_s() is subformula.left_operand().to_s():
            self.find_in_cs(subformula.left_operand(), subformula.right_operand())

    def resolve_mult(self, proof_term, subformula):
        left = proof_term.left_operand()
        right = proof_term.right_operand()
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
