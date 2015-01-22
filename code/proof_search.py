from tree import Tree
from helper import *


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
        self.cs = cs
        self.formula = formula
        self.atoms = None
        self.musts = {}
        if formula:
            self.atoms = self.atomize()
            for atom in self.atoms:
                self.musts[atom] = Tree.musts(atom)

    def set_formula(self, formula):
        self.formula = formula
        self.atoms = self.atomize()
        for atom in self.atoms:
            self.musts[atom] = Tree.musts(atom)

    def set_cs(self, cs):
        self.cs = cs

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
        splits = Tree.sum_split(self.formula)

        # second step: simplify formula if top operation is bang
        for formula in splits[:]:
            splits.remove(formula)
            new_formula = Tree.simplify_bang(formula)
            if new_formula:
                splits.append(new_formula)

        # third step: remove formulas where '!' is left child of '*'
        for formula in splits[:]:
            if Tree.has_bad_bang(formula):
                splits.remove(formula)
        return splits

    def conquer(self):
        '''
        Check if formula is satisfiable. Should only be called, if atoms and musts for ProofSearch are set.
        Returns the first atomic formula with configuration table that is satisfiable.
        @see #conquer_all_solutions

        :return atomic_formula, table: String, List
        '''
        assert self.atoms

        for atomic_formula in self.atoms:
            table = self.conquer_one(atomic_formula)
            if table:
                return atomic_formula, table
        return None

    def conquer_all_solutions(self):
        '''
        Check if formula is satisfiable. Should only be called, if atoms and musts for ProofSearch are set.
        Same as conquer, but doesn't stop at the first solution, instead it goes on and collects all proofs.

        :return solutions: List
            List contains tuples as in #conquer
        '''
        all = []
        for atomic_formula in self.atoms:
            musts = self.musts[atomic_formula]
            table = self.conquer_one(musts)
            if table:
                all.append((atomic_formula, table))
        return all

    def conquer_one(self, atom):
        '''
        Checks one atomic formula for satisfiability.
        Asserts that self.musts is already set.

        There are two important steps:

            1. Look up all possible entries in cs that can match form of a 'must'.
            If there are X-Wilds a configuration is returned, that says, which Xn corresponds to which formula/constant.
            Also if there are Y-Wilds a second argument, that gives restrictions to the choice of the wild value is
            returned.

            Example
                must = [('a', ((b:X3)->(X2->F)), ...]
                cs['a'] = ['((b:B)->(C->F)), 'A', '(Y1->(Y2->Y3))', ...]

                => config_for_one_must =
                    [({'X1':'', 'X2':'C', 'X3':'B'}, [('X2', 'X1'),... ]), ... ]
                    [({'wilds configurations},       [conditions for this configuration]

            2. One 'must' may have several configurations, but some can be in contradiction with the configurations of
            other 'musts'. So the configurations of a 'must' get merged to the previous ones. In a merge, the conditions
            must be upheld.

            Example
                config_for_one_must =       [({'X1':'', 'X2':'C', 'X3':'B'}, [('X2', 'X1'),... ]), ... ]
                config_for_one_must_new =   [({'X1':'C', 'X2':'', 'X3':''}, [('X3', 'B'),... ]), ... ]

                => merge_two_tables =       [({'X1':'C', 'X2':'C', 'X3':'B'}, []), ...]

        :param atom: atomic formula, e.g. '((a*b)*(!c))'.
        :return: finale_table, if there is a possible configuration.
        '''
        max_x = x_size(self.musts[atom])
        finale_table = [(['']*max_x, [])]

        # each entry of 'musts' has to be satisfiable!
        for entry in self.musts[atom]:  # [('a': '(A->B)'), ...]
            proof_constant = entry[0]   # 'a'
            term = entry[1]             # '(A->B)'

            configs_for_one_must = self.look_up_in_cs(proof_constant, term)

            # if there is no entry in CS that fits the term, this must is not satisfiable.
            if configs_for_one_must is None:
                return None
            else:
                # restructuring data
                configs_for_one_must = configs_to_table(configs_for_one_must, max_x)
                # merge configuration with those of previous 'musts'
                finale_table = merge_two_tables(finale_table, configs_for_one_must)

        return finale_table

    def look_up_in_cs(self, proof_constant, orig_term):
        '''
        Finds all possible configuration for a given term pair by looking up the proof_constant in CS.

        wilds:
            If there are 'Xn' in the term, so-called 'wilds' will be returned. It will connect a 'Xn' to a value found
            in CS, if the rest of the term fits the one from CS.

        conditions:
            As a consequence of 'Yn' in CS, different kind of conditions may apply to one configuration. The condition
            may connect one 'Xn' to a constant, to another 'Xm' or to a 'Yn' itself. 'Yn' can freely be chosen, as long
            as all 'Yn' have the same value for one selection.

        :param proof_constant: String
        :param orig_term: String
        :return: List
        =>  [({wilds},      [conditions]),   ({...}, [...]),                ...]
        '''

        matches_for_proof_constant = []
        cs_options = self.cs.get(proof_constant)

        # If there are entries for the given proof constant.
        if cs_options:

            # Compare each cs_term with the given original term.
            for cs_term in cs_options:

                condition, wilds = Tree.compare(Tree(orig_term).root, Tree(cs_term).root, [], {})

                # A match (with or without wilds) is possible
                if condition is not None and wilds is not None:
                    matches_for_proof_constant.append((wilds, condition))

            # If there is a least one match, even if it needs no wilds, we return a list.
            if len(matches_for_proof_constant) > 0:
                # remove emtpy entries
                matches_for_proof_constant[:] = (value for value in matches_for_proof_constant if value != ({}, []))
                return matches_for_proof_constant

        # There are no entries for the given proof constant.
        else:
            return None


def apply_condition(config, condition):
        '''
        Checks if a condition given to a configuration is ok. The outcome can either be:
            - Something in the condition is in contradiction to the configuration.
            - The condition gives no contradiction but neither can it be discarded yet.
            - The condition is possible and is no longer needed.

        :param config: List. Example: ['', '(A->B)', '']
        :param condition: Tuple. Example: ('X2', '(X1->Y2)')

        :return config: List or None. May differ from given param. Example: ['A', '(A->B), '']
        :return condition: Tuple or None. May differ from given param.
        :return y_wilds: Dict or None. Y-Wilds in here must be replaced in other conditions.
        '''
        x_index = int(condition[0][1:])-1
        config_term = config[x_index]
        condition_term = update_condition_with_x(condition[1], config)

        # If config_term is not empty, it contains only constants. In that case we can determine all
        # X's and Y's that occur in condition_term if there are any. If there are no wilds simply check
        # if config_term and condition_term are the same, else get all remaining X's and Y's.
        if config_term != '':
            conds, wilds = Tree.compare(Tree(condition_term).root, Tree(config_term).root, [], {})
            if wilds is not None:
                assert conds == []
                y_wilds = {}
                for key in wilds:
                    if key[0] == 'X':
                        i = int(key[1:])-1
                        if wilds[key] == config[i] or config[i] == '':
                            config[i] = wilds[key]
                        else:
                            return None, None, None
                    elif key[0] == 'Y':
                        y_wilds[key] = wilds[key]
                return config, None, None if y_wilds == {} else y_wilds
            else:
                return None, None, None
        # If config_term is empty the only chance to solve the condition is, if the condition consists
        # only of constants. If that is the case it can be put into config and the condition may be
        # dismissed. Else nothing more can be done.
        elif config_term == '':
            if 'X' not in condition_term and 'Y' not in condition_term:
                config[x_index] = condition_term
                return config, None, None
            else:
                return config, (condition[0], condition_term), None


def apply_all_conditions(config, conditions):
    todo_conditions = list(conditions)
    updated_config = config
    remaining_conditions = []

    while todo_conditions:
        current_condition = todo_conditions.pop()
        updated_config, mod_conditions, y_wilds = apply_condition(config, current_condition)

        if updated_config:
            # If mod_condition is not None, then there is no contradiction with the current
            # config, but it must be kept for later.
            if mod_conditions:
                remaining_conditions.append(mod_conditions)
            # If there are y_wilds, then condition_term has been match to a constant, meaning
            # either the match worked and thus the current condition is not needed anymore, or
            # else the match would not have worked and we wouldn't be here :)
            if y_wilds:
                # update all relevant conditions
                updated_conditions = get_all_with_y(todo_conditions, y_wilds.keys()) \
                                     + get_all_with_y(remaining_conditions, y_wilds.keys())
                for key in y_wilds:
                    updated_conditions = update_y(updated_conditions, key, y_wilds[key])
                # Add updated conditions to the todo_conditions.
                todo_conditions = todo_conditions + updated_conditions
        else:
            break
    return updated_config, remaining_conditions


def full_merge_of_two_configs(first, second):
    # print('-----------------')
    merge = simple_merge(first[0], second[0])
    if merge:
        merge_first, conditions_first = apply_all_conditions(merge, first[1])
        merge_second, conditions_second = apply_all_conditions(merge, second[1])
        # print(conditions_first)
        # print(conditions_second)
        # print('')
        if merge_first and merge_second:
            full_merge = simple_merge(merge_first, merge_second)
            if full_merge:
                final_merge, final_conditions = apply_all_conditions(full_merge, conditions_first + conditions_second)
                if final_merge:
                    return final_merge, final_conditions
    return None, None


def merge_two_tables(first, second):
    '''
    For two given configuration tables (with conditions!) merge them into one configuration table, if possible.
    First step of the merge is to see, if the wilds of the two table are in no contradiction.
    Second step is to check, if there is a contradiction with the given conditions (see #_apply_conditions).

    Example (without conditions, for more simple demonstration)

        t1 = [(['D', 'C', '', 'B', ''], []),
              (['C', 'C', '', 'C', ''], [])]
        t2 = [(['D', '', '', '', 'A'], []),
              (['A', '', '', '', 'D'], [])]

        => [(['D', 'C', '', 'B', 'A'], [])]

    :param first: List
    :param second: List
    :return merged_table: List
    '''
    merged_table = []
    for first_tpl in first:
        for second_tpl in second:
            table, conditions = full_merge_of_two_configs(first_tpl, second_tpl)
            if table:
                t = (table, conditions)
                merged_table.append(t)
    return uniq(merged_table)



