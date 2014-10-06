from tree import Tree


class CS:

    def __init__(self, cs):
        self._dict = cs

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
        cs_option = self._dict.get(proof_constant)

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









