from formula_tools import *
import copy


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
        conquer simply calls _conquer_one_atom on every available atom and summarizes the result.
        For preciser information see documentation in _conquer_one_atom.

        :return result: bool
            True, False for the provability of the given formula.
        :return proof: dict
            If the formula is provable, this dictionary contains the valid configurations for each atom.
        '''
        proof = {}
        result = False
        for atom in self.atoms:
            proof[atom] = summarize(self._conquer_one_atom(atom))
            if proof[atom] is not None:
                result = True
        return result, proof

    def _conquer_one_atom(self, atom):
        '''
        This method brings together the overall procedure for the conquer part of this algorithm.
        Since it needs to collect a lot of possible solutions and evaluate them, it is easy to loose
        the overview about what data is stored where.

        Example of the container that holds all information:
        all_conditions  = {must: proofs_for_atoms, ...}
                        = {(a, X1->F): [{X1: {F, Y2, ..}}, {}, ..], ...}

        For precise understanding of the procedure please read the inline comments.

        :param atom: string
            Example: ((a*b)*(!a)):F, with this the 'musts' from the atom can be accessed.
            For the example given here they would look like this:
                [(a, X3->(b:X2->F)), (b, X2), (b, X3)]
            Those musts will each be matched with entries in the cs-list that have the same proof constant.
        :return merged_conditions: list
            This list contains all possible solutions for the given atom. It is a list containing a
            condition dictionary for every valid configuration.
            Example: [{X1: Y2, X2: F, ..},  {X1: A, X2: F, ...}]
        '''
        all_conditions = defaultdict(set)

        # Collect all conditions for each must.
        # Example: a - proof_constant, X1->F - condition_term
        for proof_constant, condition_term in self.musts[atom]:

            # List that will hold all valid matches from the
            # cs-list with the current must.
            proofs_for_atom = []

            # Get all cs-entries that match the proof_constant of the must
            # and compare them with the condition_term.
            for cs_term in self.cs[proof_constant]:

                # Try to get a valid configuration for the match between the
                # current cs-term and the must.
                configuration = match_with_cs_term(cs_term, condition_term)
                if configuration is not None:
                    proofs_for_atom.append(configuration)

            # If at least one match between the condition_term and an entry in
            # cs was found we can go on. If nothing fits, the whole atom is not
            # provable.
            if proofs_for_atom:
                all_conditions[(proof_constant, condition_term)] = proofs_for_atom
            else:
                return None

        # We have now one or more possible configurations per must.
        # Now we need to find configuration that is compatible with at least one
        # configuration of all musts.
        merged_conditions = []
        for must in self.musts[atom]:
            merged_conditions = merge_conditions(all_conditions[must], merged_conditions)
            # If at some stage there is no entry left in merged_conditions, it means
            # that the previous encountered configurations of the musts are not compatible
            # with each other and thus the atom is not provable.
            if merged_conditions is None:
                return None

        return merged_conditions


def match_with_cs_term(cs_term, condition_term):
    '''
    Helper to make _conquer_one_atom easier to read.

    :param cs_term: string
    :param condition_term: string
    :return configuration: dict <set>
    '''
    # Get conditions if a match is possible.
    match = unify(cs_term, condition_term)
    if match is not None:
        # Try to resolve those conditions
        resolve_match = resolve_conditions(match)
        if resolve_match is not None:
            # Return configurations derived from the conditions.
            return resolve_match
    # Somewhere something was not valid and
    # therefore the match did not work.
    return None


def merge_conditions(conditions_to_add, existing_conditions):
    '''
    This method is used by the _conquer_one_atom method. It tries to so merge an
    existing set of conditions with a new set of conditions.

    Each list contains a dict with the different conditions inside.

    :param conditions_to_add: list
    :param existing_conditions: list
    :return combined_conditions: list
    '''
    # This is for the initial case, when there are no conditions yet. As a consequence
    # it is automatically valid with the new given conditions.
    if not existing_conditions:
        return conditions_to_add

    combined_conditions = []
    for existing in existing_conditions:
        for new in conditions_to_add:
            match = resolve_conditions(add_dicts(existing, new))
            if match:
                combined_conditions.append(match)
    if combined_conditions:
        return combined_conditions
    else:
        return None


def add_dicts(dct1, dct2):
    '''
    Helper method to simply add two dictionary together.
    Since 'update' from 'set' makes changes in place deep
    copies from both dictionaries are used.

    :param dct1: dict <set>
    :param dct2: dict <set>
    :return dct1_tmp: dict <set>
    '''
    dct1_tmp = defaultdict(set, copy.deepcopy(dct1))
    dct2_tmp = defaultdict(set, copy.deepcopy(dct2))
    all_keys = list(set(list(dct1_tmp.keys()) + list(dct2_tmp.keys())))
    for key in all_keys:
        dct1_tmp[key].update(dct2_tmp[key])
    return dct1_tmp


def summarize(conquered_atom):
    '''

    :param conquered_atom:
    :return:
    '''
    if conquered_atom is None:
            return None
    all = []
    for possible_solutions in conquered_atom:
        table = []
        for tpl in condition_dict_to_list(possible_solutions)[:]:
            if 'X' in tpl[0] and tpl[0] == tpl[1]:
                table.append((tpl[0], ''))
            elif 'X' in tpl[0]:
                table.append(tpl)
        if table:
            all.append(sorted(table))
    return all