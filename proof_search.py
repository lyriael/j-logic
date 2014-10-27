from tree import Tree
from helper import x_size
from helper import merge
from helper import unique_wilds
from helper import configs_to_table


class ProofSearch:
    '''
    Prepares the steps for the actual stuff that needs to be done.
    '''

    def __init__(self, cs, formula):
        '''
        expect a string as formula
        '''
        # todo: doku
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
            if Tree.has_outer_bang(formula):
                splits.remove(formula)
                new_formula = Tree.simplify_bang(formula)

                if new_formula:
                    splits.append(new_formula)

        # third step: remove formulas where '!' is left child of '*'
        for formula in splits[:]:
            if Tree.has_bad_bang(formula):
                splits.remove(formula)
        return splits

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

            configs_for_one_must = self._find_all_for(proof_constant, term)

            # if there is no entry in CS that fits the term, this must is not satisfiable.
            if configs_for_one_must is None:
                return None
            else:
                # restructuring data
                configs_for_one_must = configs_to_table(configs_for_one_must, max_x)
                # merge configuration with those of previous 'musts'
                finale_table = ProofSearch.merge_two_tables(finale_table, configs_for_one_must)

        return finale_table

    def conquer(self):
        '''
        Should only be called if divide was called before.
        # todo: doku
        :return:
        '''
        #todo: remove?
        # atomic_formula: '(d:F)'
        for atomic_formula in self.atoms:
            # procedure for each possible option
            table = self.conquer_one(atomic_formula)
            if table:
                return atomic_formula, table
        return None

    def conquer_all_solutions(self):
        '''
        Should only be called if divide was called before.
        Same as conquer, but doesn't stop with first solution

        # todo: doku
        :return:
        '''
        #todo: remove?
        all = []
        # atomic_formula: '(d:F)'
        for atomic_formula in self.atoms:
            # procedure for each possible option
            musts = self.musts[atomic_formula]
            max_x = x_size(musts)
            table = self.conquer_one(musts)
            if table:
                all.append((atomic_formula, table))
        return all

    @staticmethod
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
        # holds all matches
        merged_table = []

        # try to merge each configuration from the first table with each configuration from the
        # the second table.
        for tpl in first:
            for candidate_tpl in second:

                # Try simple merge, and collect all conditions that must be count for this
                # merge.
                simple_merge = merge(tpl[0], candidate_tpl[0])
                conditions = tpl[1] + candidate_tpl[1]

                # If a simple merge is not possible, we can move on the the next combination.
                if simple_merge is None:
                    pass

                # A simple merge is possible, so now it must be checked for the conditions.
                else:

                    # conditions apply to merge, oh noes..
                    if conditions:
                        todo_conditions = list(conditions)
                        done_conditions = []
                        updated_merge = simple_merge

                        # check every condition
                        while todo_conditions:
                            current_condition = todo_conditions.pop()
                            updated_merge, delete_condition = ProofSearch._apply_condition(updated_merge, current_condition)

                            # The merge is possible and ...
                            if updated_merge:

                                # ... condition is fulfilled and therefore no longer needed.
                                # (There is actually nothing more to done; the condition was 'deleted', when we used
                                # 'pop'.)
                                if delete_condition is True:
                                    pass

                                # ... condition does not matter in this merge, but it might be needed later on
                                # for another merge.
                                if delete_condition is False:
                                    done_conditions.append(current_condition)

                                # ... condition can be fulfilled, but it caused changes in 'updated_merge' and thus
                                # all related other conditions must be checked again.
                                elif isinstance(delete_condition, dict):
                                    #todo: get whats going on here
                                    change_and_todo = (get_all_with_y(todo_conditions, delete_condition.keys()) +
                                                       get_all_with_y(done_conditions, delete_condition.keys()))
                                    for key in delete_condition:
                                        change_and_todo = update_y(change_and_todo, key, delete_condition[key])
                                    todo_conditions = todo_conditions + change_and_todo

                            # The merge is not possible with this condition.
                            if not updated_merge:
                                updated_merge = None
                                break

                        # All conditions were successful apply, else 'updated_merge' would be 'None'.
                        if updated_merge:
                            merged_table.append((updated_merge, done_conditions))

                    # There are no conditions, so we're done for this combination.
                    else:
                        merged_table.append((simple_merge, []))

        # If the merge was not successful, an empty table will be returned.
        return merged_table

    @staticmethod
    def _apply_condition(merged: list, condition: tuple):
        '''

        :param merged:
        :param condition:
        :return:
        '''
        index = int(condition[0][1:])-1
        condition_term = condition[1]
        # ################
        # ('X2', '(A->B)')
        # ################
        if 'X' not in condition_term and 'Y' not in condition_term:
            # matches what's already there, or empty
            # print(condition_term)
            # print(merged[index])
            if condition_term == merged[index] or merged[index] == '':
                merged[index] = condition_term
                return merged, True
            else:
                return None, None
        # #################
        # ('X1', '(X2->F)')
        # #################
        if 'X' in condition_term and 'Y' not in condition_term:
            # print(merged[index])
            # if 'X1' != ''
            if merged[index]:
                # compare value of 'X1' with condition_term.
                con, wild = Tree.compare_second_try(Tree(condition_term).root, Tree(merged[index]).root, [], {})
                # print(wild)
                # print(con)
                # assert there are no conditions, check if the wilds fit merged.
                assert con == []
                tmp = list(merged)
                for key in wild:
                    i = int(key[1:])-1
                    if wild[key] == merged[i] or merged[i] == '':
                        tmp[i] = wild[key]
                    else:
                        return None, None
                return tmp, True
            # if 'X1' = ''
            else:
                # see if for all occurring 'Xn' in condition_term are already set.
                xs_in_condition = unique_wilds(condition_term)
                tmp = str(condition_term)
                for x in xs_in_condition:
                    i = int(x[1:])-1
                    if merged[i] == '':
                        return merged, False
                    else:
                        tmp = tmp.replace(x, merged[i])
                merged[index] = tmp
                return merged, True
        # ####################
        # if ('X1', '(Y1->F)')
        # ####################
        if 'X' not in condition_term and 'Y' in condition_term:
            # if 'X1' != ''
            if merged[index]:
                # because this method was not intended for what what I'm doing now, here's a little bit of hacking
                # that's doesn't seem to make sense.
                y_to_x_condition_term = str(condition_term.replace('Y', 'X'))
                con, wild = Tree.compare_second_try(Tree(y_to_x_condition_term).root, Tree(merged[index]).root, [], {})
                # print(con)
                # print(wild)
                if wild is None:
                    assert con is None
                    return None, None
                else:
                    assert con == []
                    y_wild ={}
                    for key in wild:
                        y_wild['Y'+key[1:]] = wild[key]
                    return merged, y_wild
            else:
                # if there is no value in 'X1' then 'Y' doesn't matter
                return merged, False
        # ####################
        # if ('X1', '(Y1->F)') !!! THIS SHOULD (HOPEFULLY) NEVER HAPPEN !!!
        # ####################
        if 'X' in condition_term and 'Y' in condition_term:
            print('This should have never happened...')
            assert False

    def _find_all_for(self, proof_constant, orig_term):
        '''
        :param proof_constant:
        :param orig_term:
        :return:
        =>  [({wilds},      [conditions]),   (...), ...]
            [ (first proof_constant-match),  (second proof_constant_match), ...]
        '''
        #todo: more doku
        found_at_least_one = False
        matches_for_proof_constant = []
        cs_option = self.cs.get(proof_constant)

        if cs_option:
            for cs_term in cs_option:
                condition, wilds = Tree.compare_second_try(Tree(orig_term).root, Tree(cs_term).root, [], {})
                if condition is not None and wilds is not None:
                    matches_for_proof_constant.append((wilds, condition))
                    found_at_least_one = True
            if found_at_least_one:
                # remove emtpy entries
                # todo: what does this line on code mean?
                matches_for_proof_constant[:] = (value for value in matches_for_proof_constant if value != ({}, []))
                return matches_for_proof_constant
        else:
            return None


def get_all_with_y(conditions, keys):
    '''
    Elements will be removed from list!
    :param conditions:
    :param keys:
    :return:
    '''
    result = []
    for con in conditions[:]:
        # check in con[1] if anything from keys occurrs
        if any(y in con[1] for y in keys):
            conditions.pop()
            result.append(con)
    return result


def update_y(conditions, key, value):
    '''

    :param conditions:
    :param wilds:
    :return:
    '''
    result = []
    for con in conditions:
        if key in con[1]:
            result.append((con[0], con[1].replace(key, value)))
        else:
            result.append((con[0], con[1]))
    return result




