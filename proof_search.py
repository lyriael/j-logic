from formula import Formula
from tree import Tree
from helper import init_dict
from helper import size
from helper import merge



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

    def merge_configurations(self, musts):
        # list of tuples, already sorted by size.
        table = self.configurations_to_table(musts)

        matches = [['']*size(musts)]
        temp = []

        # each tuple in table
        for tup in table:
            print(tup[0])
            terms = tup[1]

            if len(matches) > 0:
                for candidate in matches:
                    for term in terms:
                        m = merge(term, candidate)
                        if m:
                            temp.append(m)
                matches = list(temp)
                temp = []
                print('matches')
                print(matches)
                print('----')
            else:
                #todo: this exit is not taken!!
                return None
        return matches

    def configurations_to_table(self, musts):
        '''
        musts: list of tuples
        e.g.
        [('a','F'), ('a', 'X1'), ('b', '(X2->F))']
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
        Returned is a tuple with the constant at first place and
        all lists that match term to the corresponding in cs in the second place.

        Example:

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
        cs = self._cs[const]

        # init empty matrix of needed size
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
        # make a tuple
        t = (const, configs)
        return t











