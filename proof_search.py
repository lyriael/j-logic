from formula import Formula
from cs import CS
from tree import Tree
from helper import size
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
        -> {'(d:F)':            [('d', 'F')],
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

        :return:
        '''
        for atomic_formula in self._atomics_and_musts:
            # procedure for each possible option
            max_x = size(atomic_formula)
            tables = []
            for proof_constant_condition in atomic_formula:
                proof_constant = proof_constant_condition[0]
                condition_term = proof_constant_condition[1]
                # result of search can be True, False, or a List with wilds.
                result = self._cs.find(proof_constant, condition_term)
                # If one of the conditions for a proof_constant is not satisfiable, the whole atomic formula is
                # unsatisfiable.
                if result is False:
                    # todo: break looks ugly, but ok?
                    break
                # exact match, or wild matches with Y's. We don't need to know how, we just need to know it worked.
                elif result is True:
                    # todo: this information must be saved somewhere!
                    pass
                # there are wilds.
                else:
                    tables.append(configs_to_table(result, max_x))
            # todo: merge tables (if it is not emtpy)
            # todo: break, if merge fails or never was true






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


    # DEPRECATED
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
        x = size(musts)
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











