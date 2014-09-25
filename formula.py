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
        parts = self._sum_split()

        # second step: simplify formula if top operation is bang
        for f in parts[:]:
            if f._tree.root.left.token == '!':
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

    def _sum_split(self):
        '''
        Transforms formula to a disjunctive form.
        algorithm:

        search for first '+'
            if there is none you're done.
            if there is one, split the formula and repeat the step above for both parts.

        :return:
        List of Formulas.

        Example:
        ((a+b):F) => [a:F, b:F]

        Remark:
        If no sum exists in the formula, the returned list will simply contain the same formula.
        A empty List should never be returned.
        '''
        proof_term = Formula(self._tree.subtree(self._tree.root.left).to_s()) # Formula
        subformula = self._tree.subtree(self._tree.root.right).to_s() # String
        done = []
        todo = [proof_term._tree]
        while len(todo) > 0:
            f = todo.pop()
            if f.first('+') is None:
                done.append(f)
            else:
                left = f.deep_copy()
                node = left.first('+')
                left.left_split(node)
                todo.append(left)

                right = f.deep_copy()
                node = right.first('+')
                right.right_split(node)
                todo.append(right)
        # make to string and remove duplicates
        temp = []
        for tree in done:
            temp.append('('+tree.to_s()+':'+subformula+')')
        temp = list(set(temp))
        # make to Formulas
        formulas = []
        for s in temp:
            formulas.append(Formula(s))
        return formulas

    def _simplify_bang(self):
        '''
        Simplify Formula by resolving top '!'.

        restriction:
        - Must only be called on a Formula where top operation is ':' and to left operation is '!'.

        :return:
        new Formula,    if resolvable
        None,           if not resolvable

        Example:
        ((!(a)):(a:F))  => (a:F)
        ((!(b)):F)      => None
        '''
        # accessing child of '!'
        left = self._tree.subtree(self._tree.root.left.right)
        right = self._tree.subtree(self._tree.root.right.left)
        if right and left.to_s() == right.to_s():
            subformula = self._tree.subtree(self._tree.root.right.right)
            s = '('+right.to_s()+':'+subformula.to_s()+')'
            return Formula(s)
        else:
            return None

    def _has_bad_bang(self):
        '''
        Checks if there is a left '!' of '*' somewhere in the Formula.

        restriction:
        - Must only be called on a Formula where top operation is ':'.
        :return:
        '''
        proof_term_tree = Tree(self._tree.root.left.to_s())
        if proof_term_tree.has_bad_bang():
            return True
        else:
            return False
