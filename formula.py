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

    def proof_term(self):
        '''
        Returns a new formula that contains only the left subtree
        '''
        if self.op == ':':
            return Formula(self.tree.subtree(self.tree.root.left).to_s())
        else:
            return None

    def to_pieces(self):
        # first step: make sum-splits
        todo = []
        done = []
        todo.append(self.proof_term())

        while len(todo) > 0:
            f = todo.pop()
            if f.tree.first('+') is None:
                done.append(f)
            else:
                left = f.tree.deep_copy()
                node = left.first('+')
                left.left_split(node)
                todo.append(Formula(left.to_s()))

                right = f.tree.deep_copy()
                node = right.first('+')
                right.right_split(node)
                todo.append(Formula(right.to_s()))
        return done

