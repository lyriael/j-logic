from node import Node
from helper import parse


class Tree(object):

    def __init__(self, formula):
        self.root = Node()
        self.parse_formula(formula)

    def parse_formula(self, formula):
        term = parse(formula)
        current = self.root
        current.set_root()

        for item in term:
            if item in [':', '+', '*', '->']:
                current.token = item
                current = current.new_right()
            elif item == '!':
                current = current.parent
                current.token = item
                current.left = None
                current = current.new_right()
            elif item == '(':
                current = current.new_left()
            elif item == ')':
                current = current.parent
            else:
                current.token = item
                current = current.parent

    def to_s(self):
        '''
        Returns formula as a String using inorder.
        '''
        term = ''
        return self._inorder(self.root)

    def _inorder(self, node):
        term = ''
        if not node.is_leaf():
            term += '('
            if node.has_left():
                term += self._inorder(node.left)
        term += node.token
        if node.has_right():
            term += self._inorder(node.right) + ')'
        return term
