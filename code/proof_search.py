from formula_tools import *


class ProofSearch:
    '''
    Checks for satisfiability for a given formula and a cs list.

    Example:
        cs = {'a' : ['A', '(A->B)'], 'b' : ['(b:B)', '(A->B)'], 'c' : ['(Y1->(Y2->Y1))']}
        formula = '((((a*b)+c)*((!a)+(b*c))):F)'

    Make sure to set braces right. There is no input check.
    Possible operations for proof constants: '+', '*' and '!'.
    Possible operations for formulas: '->'
    '''

    def __init__(self, cs, formula):
        '''
        If formula is given, it will be split into atomic formulas right away.

        :param cs: dict
        :param formula: string
        :return self: ProofSearch
        '''
        self.cs = defaultdict(list, cs)
        self.formula = formula
        self.atoms = None
        self.musts = {}
        if formula:
            self.atoms = self.atomize()
            for atom in self.atoms:
                self.musts[atom] = musts(atom)

    def atomize(self):
        '''
        If possible the formula is split into several smaller parts. It is comparable with transforming a formula
        into disjunctive form. The original formula is exactly then satisfiable, if at least one of the atomic formulas
        are satisfiable.

        -   For each '+', the formula will be split in two corresponding parts. So for the formula to be provable, only
            one of these subformulas must be provable.

        These splits are further sorted:
        -   If a '!' is top operation of a formula, the formula is simplified by correctly removing the '!' if possible.
            If this is not possible, the subformula is not provable and will be deleted.
        -   If a '!' is a left child of '*' the (sub)formula is not provable, and so the subformula will be deleted.

        :return: list
            containing atomic formulas as Strings.
            Example: '((!d)+((a*b)+c))' => ['(a*b)', 'c']
        '''
        # first step: make sum-splits
        splits = sum_split(self.formula)

        # second step: simplify formula if top operation is introspection
        for formula in splits[:]:
            splits.remove(formula)
            new_formula = simplify_introspection(formula)
            if new_formula:
                splits.append(new_formula)

        # third step: remove formulas where '!' is left child of '*'
        for formula in splits[:]:
            if has_bad_introspection(formula):
                splits.remove(formula)
        return splits

    def conquer(self):
        '''
        :return result: bool
        :return proof: dict
        '''
        # todo: DOC
        proof = {}
        result = False
        for atom in self.atoms:
            proof[atom] = nice(self._conquer_one_atom(atom))
            if proof[atom] is not None:
                result = True
        return result, proof

    def _conquer_one_atom(self, atom):
        '''
        :param atom: string
        :return merged_conditions: list
        '''
        # todo: DOC
        all_conditions = defaultdict(set)
        # Collect all conditions for each must.
        for proof_constant, condition_term in self.musts[atom]:
            proofs_for_atom = []
            # compare the condition_term with all available entries in cs.
            for cs_term in self.cs[proof_constant]:
                match = unify(cs_term, condition_term)
                if match is not None:
                    resolved = resolve_conditions(match)
                    if resolved is not None:
                        proofs_for_atom.append(resolved)
            # if at least one match between the condition_term and an entry in cs was found.
            if proofs_for_atom:
                all_conditions[(proof_constant, condition_term)] = proofs_for_atom
            # no possible match. All is lost.
            else:
                return None
        merged_conditions = []
        # We must now merge the possible configs together. We will add one set of configs of a must to the existing
        # merged before.
        for must in self.musts[atom]:
            merged_conditions = combine(all_conditions[must], merged_conditions)
            if merged_conditions is None:
                return None
        return merged_conditions



