from helper import parse


class Node(object):

    def __init__(self):
        self._token = 'no token'
        self._parent = self
        self._left = None
        self._right = None

    def __len__(self):
        return self._len_helper()

    def __str__(self):
        return self.inorder()

    def is_root(self):
        return self._parent == self

    def is_leaf(self):
        return self._left is None and self._right is None

    def is_tree(self):
        return len(self.root()) > 1

    def has_left(self):
        return self._left is not None

    def has_right(self):
        return self._right is not None

    def right(self):
        return self._right

    def left(self):
        return self._left

    def root(self):
        if self._parent == self:
            return self
        else:
            return self._parent.root()

    def token(self):
        return self._token

    def value(self):
        return self._token

    def parent(self):
        return self._parent

    def new_left(self):
        new_left = Node()
        new_left._parent = self
        self._left = new_left
        return new_left

    def new_right(self):
        new_right = Node()
        new_right._parent = self
        self._right = new_right
        return new_right

    def inorder(self):
        term = ''
        if self.has_left():
            term += '(' + self._left.inorder()

        term += self._token

        if self.has_right():
            term += self._right.inorder() + ')'

        if self._token == '!':
            term = term[:-1]
        return term

    def subtree(self):
        subterm = self.inorder()
        return Node.make_tree(subterm)

    @staticmethod
    def make_tree(term):
        term = parse(term)
        root = Node()
        current = root

        for item in term:
            if item in [':', '+', '*', '->']:
                current._token = item
                current = current.new_right()
            elif item == '!':
                current._token = item
                current = current.new_right()

            elif item == '(':
                current = current.new_left()
            elif item == ')':
                current = current._parent

            else:
                current._token = item
                current = current._parent
                if current._token == '!':
                    current = current._parent
        return root

    # private methods
    def _len_helper(self):
        count = 0
        if self.has_left():
            count += self._left._len_helper()

        count += 1

        if self.has_right():
            count += self._right._len_helper()

        return count
