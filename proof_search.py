from formula import Formula
from tree import Tree
from helper import config_dict
from helper import init_dict


class ProofSearch:

    def __init__(self, cs, formula):
        '''
        expect a string as formula
        '''
        self._cs = cs
        self._formula = Formula(formula)

    def divide(self):
        # of those tiny-formulas it is enough to prove just one
        big_mama = {}
        for small in self._formula.to_pieces():
            # find how that structre looks in test_formula#test_to_pieces_and_get_terms_to_proof
            big_mama[small.formula] = small.get_terms_to_proof()
        return big_mama

    def conquer(self, musts):
        '''
        musts: list of tuples
        e.g.
        [('a','F'), ('a', 'X1'), ('b', '(X2->F))']
        all those tuples must be found in cs.
        This method should only be used on reduced formulas!
        '''
        # init key list
        #todo

    def get_configurations(self, term):
        #todo: remove
        '''
        This should not be used, since I like the other matrix better.

        Expects only term that contain wild char (e.g. X3).

        configs example:

                1       2       3       ...     for i in cs[const].
        X1: [   ''  ,   'G' ,   'H'  ,  ... ]
        X2: [   ''  ,   'A' ,   'b:B',  ... ]

        '''
        const = term[0]
        orig_formula = term[1]
        cs = self._cs[const]
        configs = config_dict(term, len(cs))

        i = 0
        for cs_formula in cs:
            match = Tree.possible_match(orig_formula, cs_formula)
            if isinstance(match, list):
                for x in match:
                    configs[x[0]][i] = x[1]
            i += 1
        return configs

    def get_other_configurations(self, term, x_size):
        '''
        Returned are all Tuples that match term to the corresponding in cs.

        x_size = 5
        len(cs) = 3

                    j
                X1  X2  X3  X4  X5
            [[  A,  A,  -,  -,  -],
            [   A,  C,  -,  -,  -],
         i  [   B, b:B, -,  -,  -]]

        It might be, that some X's place is never used, but that's ok.
        '''
        const = term[0]
        orig_formula = term[1]
        cs = self._cs[const]

        # init matrix of needed size
        configs = [['' for i in range(x_size)] for j in range(len(cs))]

        # iterate through all entries in cs for given constant of term.
        i = 0
        for cs_formula in cs:
            match = Tree.possible_match(orig_formula, cs_formula)
            if isinstance(match, list):
                for x in match:
                    j = int(x[0][1:])-1
                    configs[i][j] = x[1]
            i += 1

        for item in configs[:]:
            if item == ['']*x_size:
                configs.remove(item)
        return configs


    @staticmethod
    def merge_configurations(all_configs):
        # get a list of a occuring Xs
        wilds = []
        for c in all_configs:
            wilds += c.keys()
        wilds = list(set(wilds))

        # init returning config
        merged_config = init_dict(wilds, 0)








