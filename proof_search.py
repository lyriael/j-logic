from formula import Formula
from cs import CS
from tree import Tree
from helper import x_size
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











