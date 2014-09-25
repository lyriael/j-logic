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

    def _inorder_string(self, node):
        '''
        This is an exact copy of the same-named method in Tree.
        todo: find cleaner solution
        '''
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

    def compare_to_OLD(self, other_node):
        '''
        String comparement
        :param other_node:
        :return:
        '''
        if self.token[0] in ['X']:
            return 'wild match'
        elif self.token == other_node.token:
            return 'exact match'
        else:
            return 'no match'

    def compare_node_to(self, other_node):
        '''
        # TODO
        :param other_node:
        :return:
        '''
        #todo refactor
        matches = True
        wilds = {}
        if self.token[0] == 'X':
            wilds[self.token] = other_node.to_s()
        elif self.token[0] == 'Y':
            matches &= True

        elif self.token == other_node.token:
            matches &= True
            # check if both nodes have children
            if (bool(self.has_left()) ^ bool(other_node.has_left())) or \
                    (bool(self.has_right()) ^ bool(other_node.has_right())): # ^ == XOR
                matches &= False
            else:
                if self.has_left() and other_node.has_left():
                    m, w = self.left.compare_node_to(other_node.left)
                    matches &= m
                    wilds.update(w)
                if self.has_right() and other_node.has_right():
                    m, w = self.right.compare_node_to(other_node.right)
                    matches &= m
                    wilds.update(w)
        # no match and no wilds
        else:
            matches &= False
        return matches, wilds


