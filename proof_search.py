from tree import Tree
from helper import x_size
from helper import merge
from helper import unique_wilds


class ProofSearch:
    '''
    Prepares the stepts for the actual stuff that needs to be done.
    '''

    def __init__(self, cs, formula):
        '''
        expect a string as formula
        '''
        self._cs = cs
        self._formula = formula
        self._atomics_and_musts = {}

    def divide(self):
        '''
        Does two things:

        1. splits for + and eliminates bad placed !
        2. returns 'musts'

        For the further proof search one entry of the returning dict must be satisfiable.
        For an entry to be satisfiable, all tuples must be satisfiable.

        Example: '(((c*(a*b))+d):F)'

        -> {
            '(d:F)':            [('d', 'F')],
            '((c*(a*b)):F)':    [('a', '(X2->X1)'), ('b', 'X2'), ('c', '(X1->F)')]}
        '''
        # of those tiny-formulas it is enough to prove just one
        atomics_with_musts = {}
        atoms = self.atomize()
        for atom in atoms:
            # find how that structre looks in test_formula#test_to_pieces_and_get_terms_to_proof
            atomics_with_musts[atom.to_s()] = atom.musts()
        self._atomics_and_musts = atomics_with_musts
        return atomics_with_musts

    def conquer(self):
        '''
        Should only be called if divide was called before.
        # todo: doku
        :return:
        '''
        # atomic_formula: '(d:F)'
        for atomic_formula in self._atomics_and_musts:
            # procedure for each possible option
            musts = self._atomics_and_musts[atomic_formula]
            max_x = x_size(musts)
            table = self._conquer_one(max_x, musts)
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
        all = []
        # atomic_formula: '(d:F)'
        for atomic_formula in self._atomics_and_musts:
            # procedure for each possible option
            musts = self._atomics_and_musts[atomic_formula]
            max_x = x_size(musts)
            table = self._conquer_one(max_x, musts)
            if table:
                all.append((atomic_formula, table))
        return all

    def _conquer_one(self, max_x, musts):
        '''

        :param musts: [('a': '(A->B)'), ...]
        :return: satisfiable: True, False
        '''
        # todo: write some more tests!!
        # todo: -> may be for good testing method needs to be changed.
        finale_table = [(['']*max_x, [])]
        # each of 'must' has to be satisfiable!
        for must in musts:           # [('a': '(A->B)'), ...]
            proof_constant = must[0] #   'a'
            condition_term = must[1] #   '(A->B)'

            configs_for_one_must = self.find_all_for(proof_constant, condition_term)
            # print('\tconfigs for: ' + str(must))
            # print('\tcurrent finale table: ' + str(finale_table))
            # if configs_for_one != None => 'must' is satisfiable with no further conditions.
            if configs_for_one_must is None:
                return None
            else:
                configs_for_one_must = configs_to_table(configs_for_one_must, max_x)
                # print('\t\tas table: ' + str(configs_for_one_must))
                finale_table = ProofSearch.merge_two_tables(finale_table, configs_for_one_must)
                # print('\t\tfinale table: ' + str(finale_table))
        return finale_table

    @staticmethod
    def apply_condition(merged: list, condition: tuple):
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

    @staticmethod
    def merge_two_tables(first, second):
        '''
        :param first:
        :param second:
        :return:
        '''
        # todo: may be needs to be moved as well
        # holds all matches
        merged_tables = []
        for tpl in first:
            for candidate_tpl in second:

                simple_merge = merge(tpl[0], candidate_tpl[0])
                conditions = tpl[1] + candidate_tpl[1]

                if simple_merge:
                    # no conditions, yej!
                    if not conditions:
                        merged_tables.append((simple_merge, []))

                    # conditions apply to merge, oh noes..
                    else:
                        todo_conditions = list(conditions)
                        done_conditions = []
                        updated_merge = simple_merge

                        # check every condition
                        while todo_conditions:
                            current = todo_conditions.pop()
                            updated_merge, delete_condition = ProofSearch.apply_condition(updated_merge, current)

                            # merge can fulfills
                            if updated_merge:
                                # condition is fulfilled an no longer needed, also merge was successful.
                                if delete_condition is True:
                                    # condition was already deleted by poping it.
                                    pass
                                # condition does not matter for this merge, but might be needed later.
                                if delete_condition is False:
                                    done_conditions.append(current)
                                # condition could be fulfilled, but other conditions must be updated.
                                elif isinstance(delete_condition, dict):
                                    change_and_todo = (get_all_with_y(todo_conditions, delete_condition.keys()) +
                                                       get_all_with_y(done_conditions, delete_condition.keys()))
                                    for key in delete_condition:
                                        change_and_todo = update_y(change_and_todo, key, delete_condition[key])
                                    todo_conditions = todo_conditions + change_and_todo
                            # condition is not compatible with merge
                            if not updated_merge:
                                updated_merge = None
                                break
                        # end of 'while todo_conditions'

                        # All conditions were successful apply
                        if updated_merge:
                            merged_tables.append((updated_merge, done_conditions))
        return merged_tables

    def find_all_for(self, proof_constant, orig_term):
        '''
        :param proof_constant:
        :param orig_term:
        :return:
        =>  [({wilds},      [conditions]),   (...), ...]
            [ (first proof_constant-match),  (second proof_constant_match), ...]


        Alte Doku von find():
        :param proof_constant: constant proof term, which can be looked up in cs. Example: 'a'
        :param orig_term: required term that must be proven by key. Example: '(X1->F)'
        :return :
            [match_found, wilds]
            match_found:
                False, if key is not in present in cs, or simply no match can be found.
                True, if a exact match is found, or a wild match is possible.
            wilds: if match depends on Wilds, else empty.
                Example: [{'X1':'A','X4':'A->B'}, {'X1': ...,'X4': ..}, {...,...}]

        '''
        found_at_least_one = False
        matches_for_proof_constant = []
        cs_option = self._cs.get(proof_constant)

        if cs_option:
            for cs_term in cs_option:
                condition, wilds = Tree.compare_second_try(Tree(orig_term).root, Tree(cs_term).root, [], {})
                if condition is not None and wilds is not None:
                    matches_for_proof_constant.append((wilds, condition))
                    found_at_least_one = True
            if found_at_least_one:
                # remove emtpy entries
                matches_for_proof_constant[:] = (value for value in matches_for_proof_constant if value != ({}, []))
                return matches_for_proof_constant
        else:
            return None

    def atomize(self):
        '''
        If possible the formula is split into several smaller parts. It is comparable with transforming a formula
        into DNS.

        -   For each '+', the formula will be split in two corresponding parts. So for the formula to be provable, only
            one of these subformulas must be provable.

        These splits are further sorted:
        -   If a '!' is top operation of a formula, the formula is simplified by correctly removing the '!' if possible.
            If this is not possible, the subformula will be deleted.
        -   If a '!' is a left child of '*' the (sub)formula is not provable, and so the subformula will be deleted.

        :return:
        List with Formulas.
        '''
        # first step: make sum-splits
        parts = Tree(self._formula)._sum_split()

        # second step: simplify formula if top operation is bang
        for f in parts[:]:
            if f.root.left.token == '!':
                parts.remove(f)
                improved_f = f._simplify_bang()
                if improved_f is not None:
                    parts.append(improved_f)

        # third step: remove formulas where '!' is left child of '*'
        for f in parts[:]:
            if f._has_bad_bang(): # makes a Tree copy.
                parts.remove(f)
        return parts


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


def configs_to_table(configs, size):
    '''

    :param configs: [   ({'X1':'A', 'X3':'(A->B)'}, [('X2', 'X1')]  ),
                        ({'X1':'C', 'X3':'C'},      []              ),
                        ({...},                     []              )],
                        second return argument of cs, compare_to
    :param size: highest Xn that occurs for one atomic Formula.
    :return: table:
    Example:
              X1  X2  X3  X4    conditions
        [   ([   ,   ,   ,   ],  None)
            ([   ,   ,   ,   ],  [...])
            ...
            ([   ,   ,   ,   ],  None)
        ]
    '''
    # init empty matrix of needed size
    # e.g.: x_size = 5, len(cs) = 3
    # >> table = [(['', '', '', '', ''], []), (['', '', '', '', ''], []), (['', '', '', '', ''], [])]
    if configs:
        table = [(['' for i in range(size)], []) for j in range(len(configs))]
        row = 0
        for tpl in configs:
            for x in tpl[0]: # accessing the wild-dict, ignoring conditions (tpl[1])
                position = int(x[1:]) - 1
                term = tpl[0][x]
                table[row][0][position] = term
            row += 1
        return table
    else:
        return [(['']*size, [])]

