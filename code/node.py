class Node(object):

    def __init__(self):
        self.token = ''
        self.parent = None
        self.position = ''
        self.left = None
        self.right = None
        self.sibling = None

    def __str__(self):
        '''
        This method gives a string representation of the subtree of this node.
        To get only its value, use self.token.

        :return subtree: string
        '''
        return self._inorder_string(self)

    def is_root(self):
        return self.parent == self

    def is_leaf(self):
        return self.left is None and self.right is None

    def is_x_wild(self):
        return self.token[0] == 'X'

    def is_y_wild(self):
        return self.token[0] == 'Y'

    def has_no_wilds(self):
        return not ('X' in self.to_s() or 'Y' in self.to_s())

    def set_root(self):
        self.parent = self
        self.position = 'root'
        self.sibling = None

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

    def set_sibling(self):
        sibling = None
        if self.position == 'right':
            sibling = self.parent.left
        elif self.position == 'left':
            sibling = self.parent.right
        self.sibling = sibling
        if sibling is not None:
            sibling.sibling = self

    def set_position(self):
        if self.parent.left == self:
            self.position = 'left'
        elif self.parent.right == self:
            self.position = 'right'

    def set_left(self, node):
        self.left = node
        node.parent = self
        node.set_position()
        node.set_sibling()

    def set_right(self, node):
        self.right = node
        node.parent = self
        node.set_position()
        node.set_sibling()

    def get_root(self):
        current = self
        while not current.is_root():
            current = current.parent
        return current

    def _inorder_string(self, node):
        term = ''
        if not node.is_leaf():
            term += '('
            if node.has_left():
                term += self._inorder_string(node.left)
        term += node.token
        if node.has_right():
            term += self._inorder_string(node.right) + ')'
        return term

    def to_s(self):
        return self._inorder_string(self)

    def swap_with(self, replacement):
        replacement.position = self.position
        if replacement.position == 'left':
            self.parent.left = replacement
        else:
            self.parent.right = replacement
        replacement.parent = self.parent
        replacement.sibling = self.sibling

