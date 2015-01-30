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

        :param cs: Dict
        :param formula: String
        :return: None
        '''
        self.cs = defaultdict(list, cs)
        self.formula = formula
        self.atoms = None
        self.musts = {}
        if formula:
            self.atoms = self.atomize()
            for atom in self.atoms:
                self.musts[atom] = musts(atom)

    def set_formula(self, formula):
        self.formula = formula
        self.atoms = self.atomize()
        for atom in self.atoms:
            self.musts[atom] = musts(atom)

    def set_cs(self, cs):
        self.cs = defaultdict(list, cs)

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

        # second step: simplify formula if top operation is bang
        for formula in splits[:]:
            splits.remove(formula)
            new_formula = simplify_bang(formula)
            if new_formula:
                splits.append(new_formula)

        # third step: remove formulas where '!' is left child of '*'
        for formula in splits[:]:
            if has_bad_bang(formula):
                splits.remove(formula)
        return splits

    def conquer_one_atom(self, atom):
        '''

        :param atom: ((a*b)*(!c)):F, self.musts[atom] =
        :return: list of dicts
        '''
        all_conditions = {}
        # Collect all conditions for each must.
        for must in self.musts[atom]:
            c = []
            for term in self.cs[must[0]]:
                match = unify(term, must[1])
                if match is not None:
                    resolved = resolve_conditions(match)
                    if resolved is not None:
                        c.append(resolved)
            # if at least one match was found
            if c:
                all_conditions[must] = c
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

    def conquer_all_atoms(self):
        proof = {}
        result = False
        for atom in self.atoms:
            proof[atom] = nice(self.conquer_one_atom(atom))
            if proof[atom] != 'Not provable.':
                result = True
        return result, proof


def nice(conqured_atom):
    if conqured_atom is None:
            return 'Not provable.'
    all = []
    for possible_solutions in conqured_atom:
        table = []
        for tpl in condition_dict_to_list(possible_solutions)[:]:
            if 'X' in tpl[0] and tpl[0] == tpl[1]:
                table.append((tpl[0], ''))
            elif 'X' in tpl[0]:
                table.append(tpl)
        if table:
            all.append(sorted(table))
    return all


def combine(conditions_to_add, existing_conditions):
    '''
    :param conditions_to_add: list
    :param existing_conditions: list
    :return:
    '''
    if not existing_conditions:
        return conditions_to_add

    combined_conditiones = []
    for existing in existing_conditions:
        for new in conditions_to_add:
            match = resolve_conditions(merge_dicts(existing, new))
            if match:
                combined_conditiones.append(match)
    if combined_conditiones:
        return combined_conditiones
    else:
        return None


def merge_dicts(dct1, dct2):
    if not dct1:
        return dct2
    if not dct2:
        return dct1
    merged = defaultdict(list)
    dct1 = defaultdict(list, dct1)
    dct2 = defaultdict(list, dct2)
    all_keys = list(set(list(dct1.keys()) + list(dct2.keys())))
    for key in all_keys:
        merged[key] += dct1[key]
        merged[key] += dct2[key]
        merged[key] = sorted(list(set(merged[key])))
    return merged