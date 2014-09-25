from tree import Tree


class CS:

    def __init__(self, cs):
        self._dict = cs

    def find(self, proof_constant, orig_term):
        '''

        :param proof_constant: constant proof term, which can be looked up in cs. Example: 'a'
        :param orig_term: required term that must be proven by key. Example: '(X1->F)'
        :return :
            match_found:
                False, if key is not in present in cs, or simply no match can be found.
                True, if a exact match is found.
            List: if match depends on Wilds.
                Example: [[{'X1':'A'},{'X4', 'A->B'}], [{'X1', ...},{'X4', ..}], [{...},{...}]]
        '''
        cs_terms = self._dict.get(proof_constant, [])
        wild_config = []

        # no entry for constant => False
        if len(cs_terms) == 0:
            return False
        else:
            match_found = False
            orig = Tree(orig_term)

            for cs_term in cs_terms:
                cs = Tree(cs_term)
                # if cs_term contains a 'Y', or if orig_term has a 'X', we
                # need only to know if it matches, but are not interested,
                # how they match.
                if ('Y' in cs_term) or ('X' not in orig_term):
                    match_found = match_found | cs.compare_to(orig)
                else:
                    # if orig_term contains 'X' we need to know if a configuration
                    # is possible and what that configuration is, or there is no match.
                    match = orig.compare_to(cs)
                    if isinstance(list, match):
                        wild_config.append(match)
                    else:
                        match_found = match_found | match
        return match_found, wild_config









