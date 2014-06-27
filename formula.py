__author__ = 'lyriael'
from tree import Tree


class Formula(object):

    def __init__(self, formula):
        '''
        string as formula expected. Be careful to put all parentheses.
        '''
        self.formula = formula
        self.tree = Tree(formula)
        self.op = self.tree.root.token

    def to_pieces(self):
        '''
        Returns a list of formulas, where all '+', all top '!' and all bad '!'
        are removed.

        MAGIC HAPPENS HERE.
        '''
        # first step: make sum-splits
        parts = self.sum_split()

        # second step: simplify formula if top operation is bang
        bangs = []
        for f in parts[:]:
            if f.proof_term().op == '!':
                bangs.append(f)
                parts.remove(f)

        for f in bangs:
            improved = f.remove_bang()
            if improved is not None:
                parts.append(improved)

        # third step: remove formulas where bang is left child of mult
        for f in parts[:]:
            if f.proof_term().tree.has_bad_bang():
                parts.remove(f)
        return parts

    def get_terms_to_proof(self):
        '''
        This method is just to keep the look a bit cleaner.
        The work itself is done by Tree.

        MAGIC COMES FROM HERE SOMEWHERE.
        '''
        return self.tree.proof_terms()

    def proof_term(self):
        '''
        Returns a new formula that contains only the left subtree.
        Not to be confused with 'get_terms_to_proof()' that
        calls 'proof_terms()' from Tree.
        '''
        if self.op == ':':
            return Formula(self.tree.subtree(self.tree.root.left).to_s())
        else:
            return None

    def subformula(self):
        if self.op == ':':
            return Formula(self.tree.subtree(self.tree.root.right).to_s())
        else:
            return None

    def sum_split(self):
        proof_term = self.proof_term()
        subformula = self.subformula().formula
        done = []
        todo = [proof_term.tree]
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

    def remove_bang(self):
        # accessing child of '!'
        left = self.tree.subtree(self.tree.root.left.right)
        right = self.tree.subtree(self.tree.root.right.left)
        if right and left.to_s() == right.to_s():
            subformula = self.tree.subtree(self.tree.root.right.right)
            s = '('+right.to_s()+':'+subformula.to_s()+')'
            return Formula(s)
        else:
            return None
