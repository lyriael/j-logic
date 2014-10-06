from formula import Formula
from cs import CS
from tree import Tree
from helper import x_size
from helper import merge
from helper import configs_to_table


class ProofSearch:

    def __init__(self, cs, formula):
        '''
        expect a string as formula
        '''
        self._cs = CS(cs)
        self._formula = Formula(formula)
        self._atomics_and_musts = {}

    def divide(self):
        # todo: move divide to formula?
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
        for small in self._formula.atomize():
            # find how that structre looks in test_formula#test_to_pieces_and_get_terms_to_proof
            atomics_with_musts[small.formula] = small.get_musts()
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

            configs_for_one_must = self._cs.find_all_for(proof_constant, condition_term)
            # print('\tconfigs for: ' + str(must))
            # print('\tcurrent finale table: ' + str(finale_table))
            # if configs_for_one != None => 'must' is satisfiable with no further conditions.
            if configs_for_one_must is None:
                return None
            else:
                configs_for_one_must = configs_to_table(configs_for_one_must, max_x)
                # print('\t\tas table: ' + str(configs_for_one_must))
                finale_table = Tree.merge_two_tables(finale_table, configs_for_one_must)
                # print('\t\tfinale table: ' + str(finale_table))
        return finale_table


    # ---------------------- DEPRECATED -------------------------------------------
    def configuration_merge(self, table):
        '''
        ===DEPRECATED===
        see merge two tables in helper
        ================
        Puts all possible solutions from configuration_table together.
        The result are the possible solutions.

        :param table:
        :return:
        '''
        #todo: get number of variables in a nicer way!
        size = len(table[0][1][0])
        match = [['']*size]
        temp = []

        for look_up in table:
            samples = look_up[1]
            for candidate in samples:
                for condition in match:
                    print('compare ' + str(condition) + ' with ' + str(candidate))
                    m = merge(condition, candidate)
                    if m is None:
                        pass
                    else:
                        #print('add ' + str(m) + ' to merge.')
                        temp.append(m)
            match = temp
            temp = []
        return match

    def configuration_table(self, musts):
        '''
        ===DEPRECATED====
        see compare_to() in cs
        =================

        musts: list of tuples
        the output of this method is used in configuration_merge.

        e.g.
        [('a',['F', 'G']), ('a', ['X1']), ('b', ['(X2->F)])']
        all those tuples must be found in cs.
        This method should only be used on reduced formulas!

        Look at tests to see return example.
        '''

        # collect all configurations
        all_configs = []
        x = x_size(musts)
        for term in musts:
            all_configs.append(ProofSearch.get_configuration(self, term, x))
        return sorted(all_configs, key=lambda t: len(t[1]))

    def get_configuration(self, term, x_size):
        '''
        ===DEPRECATED====
        see compare_to() in cs
        =================
        private method!!

        Returned is a tuple with the constant at first place and
        all lists that match term to the corresponding in cs in the second place.

        Example:

        term: ('a', '(X1->(X2->F))')
        constant: 'a'
        Matrix:

        x_size = 5
        len(cs) = 3

                    j
                X1  X2  X3  X4  X5
            [[  A,  A,  -,  -,  -],
            [   A,  C,  -,  -,  -],
         i  [   B, b:B, -,  -,  -]]

         return ('a', M)

        It might be, that some X's place is never used, but that's ok.
        '''
        const = term[0]
        orig_formula = term[1]
        cs = self._cs.get(const, [])

        # If cs contains no entry for 'const'.
        if len(cs) == 0:
            no_entries = (const, [[]])
            return no_entries

        # init empty matrix of needed size
        # e.g.: x_size = 5, len(cs) = 3
        # >> configs = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]
        configs = [['' for i in range(x_size)] for j in range(len(cs))]

        # iterate through all entries in cs for given constant of term.
        i = 0
        for cs_formula in cs:
            match = Tree.match_against(orig_formula, cs_formula)
            if isinstance(match, list):
                # if there is an exact match, match is just empty and the next loop will not iterate.
                for x in match:
                    j = int(x[0][1:])-1
                    configs[i][j] = x[1]
            i += 1

        for item in configs[:]:
            if item == ['']*x_size:
                configs.remove(item)
        # make a tuple
        t = (const, configs)
        return t











