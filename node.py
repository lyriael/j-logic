
class Node(object):

    def __init__(self):
        self.token = ''
        self.position = ''
        self.parent = None
        self.left = None
        self.right = None
        self.sibling = None

    def is_lonely(self):
        return self.parent is None

    def is_root(self):
        return self.parent == self

    def is_leaf(self):
        return self.left is None and self.right is None

    def set_root(self):
        self.parent = self
        self.position = 'root'

    def new_right(self):
        right_child = Node()
        right_child.position = 'right'
        right_child.parent = self
        if self.has_left():
            self.left.sibling = right_child
            right_child.sibling = self.left
        self.right = right_child
        return right_child

    def new_left(self):
        left_child = Node()
        left_child.position = 'left'
        left_child.parent = self
        if self.has_right():
            self.right.sibling = left_child
            left_child.sibling = self.right
        self.left = left_child
        return left_child

    def has_right(self):
        return self.right is not None

    def has_left(self):
        return self.left is not None

