from tree import Tree


class CS:

    def __init__(self, cs):
        self._dict = cs

    def find(self, proof_constant, orig_term):
        '''

        :param proof_constant: constant proof term, which can be looked up in cs. Example: 'a'
        :param orig_term: required term that must be proven by key. Example: '(X1->F)'
        :return :
            [match_found, wilds]
            match_found:
                False, if key is not in present in cs, or simply no match can be found.
                True, if a exact match is found, or a wild match is possible.
            wilds: if match depends on Wilds, else empty.
                Example: [[{'X1':'A','X4':'A->B'}, {'X1': ...,'X4': ..}, {...,...}]]
        '''
        cs_terms = self._dict.get(proof_constant, [])
        wild_config = []
        # no entry for constant => False
        if len(cs_terms) == 0:
            # print('len(cs_terms) == 0:')
            # print('\t return False')
            return False, []
        else:
            match_found = False
            orig = Tree(orig_term)
            # print('len(cs_terms) > 0')

            for cs_term in cs_terms:
                # print('\t cs_term: ' + str(cs_term) )
                cs = Tree(cs_term)
                # cs_term must be compared to orig_term. If orig_term contains X,
                # a List of X-wilds might be returned.
                if 'Y' in cs_term:
                    # todo: compare_to muss noch angepasst werden.
                    match = cs.compare_to(orig)
                    if isinstance(match, dict):
                        wild_config.append(match)
                        match_found |= True
                    else:
                        match_found |= match
                else:
                    # if orig_term contains 'X' we need to know if a configuration
                    # is possible and what that configuration is, or there is no match.
                    # print('\t there is a X in orig_term: ' + str(orig_term))
                    # compare_to returns True, False or dict.
                    match = orig.compare_to(cs)
                    # print('\t match: ' + str(match))
                    if isinstance(match, dict):
                        wild_config.append(match)
                        match_found |= True
                    else:
                        match_found |= match
                # print('\t ---')
        return match_found, wild_config









