__author__ = 'lyriael'
from tree import Tree


class Formula(object):

    def __init__(self, formula):
        '''
        string as formula expected. Be careful to put all parentheses.
        '''
        self.formula = formula
        self._tree = Tree(formula)

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
        parts = self._tree._sum_split()

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

    def get_musts(self):
        '''
        Analyse Formula and put a List together with entries which must be in CS to proof the Formula. Expects the
        Formula to be atomic!
        If the Formula contains any '*', the look up entries will contain so called 'Wilds' (X1, X2, ...). These 'Wilds'
        do not exists in CS, but can be assigned any constant or formula that fits. But because any Wild can occure more
        than once for different proof constants, not every configuration is valid.

        :return:
        Alphabetically sorted List of Tuples.
        First value of a tuple is the key variable (constant), second value is a List with Formulas.
        '''
        return self._tree.musts()

