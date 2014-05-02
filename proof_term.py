from tree_node import Node

formulas =      ['(a+b):B',     '(a+b):A',  'b!:(b:B)',     '(b!+c):(b:B)',     '((a+b)+c):C']
proof_terms =   ['(a+b)',       '(a+b)',    'b!',           '(b!+c)',           '((a+b)+c)']


class ProofTerm(object):

    def __init__(self, expression):
        self.tree = Node.make_tree(expression)  # root is at index 0
        return

    def __repr__(self):
        return self.tree[0].inorder()

    def type(self):
        root = self.tree
        if root == '+':
            return 'SUM'
        elif root == '!':
            return 'BANG'
        elif root.islower():
            return 'CONSTANT'
        else:
            return 'Invalid character: ' + str(root)

    def is_constant(self):
        return self.type() == 'CONSTANT'

    def is_sum(self):
        return self.type() == 'SUM'

    def left(self):
        return str(self.tree.get_left())

    def right(self):
        return str(self.tree.get_right())

    def is_bang(self):
        return self.type() == 'CONSTANT'


tests = ['(a+b)', 'a']
test = ProofTerm('(!a+(c+!b))')
print(test)
