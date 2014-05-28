from helper import parse
__MAX_CALLS__ = 50


class Node(object):

    def __init__(self):
        self._token = '_NT_'
        self._parent = self
        self._left = None
        self._right = None

    def __len__(self):
        return self._len_helper()

    def __str__(self):
        '''
        String of tree, where current Node is root.
        '''
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

    def has_child(self):
        return self._left is not None or self._right is not None

    def is_left(self):
        return self._parent._left is self

    def is_right(self):
        return self._parent._right is self

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

    def set_root(self):
        self._parent = self

    def set_token(self, new_token):
        self._token = new_token

    def value(self):
        return self._token

    def parent(self):
        return self._parent

    def get_left(self):
        return self._left

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

    def find(self, step=0, token='!'):
        if self._token == token:
            return True
        else:
            left = False
            right = False
            if self.has_left():
                left = self._left.find(step+1)
            if self.has_right():
                right = self._right.find(step+1)
            return left or right

    def find_and_return(self, token='!'):
        if self._token == '!':
            return self
        else:
            if self.has_left():
                left = self._left.find_and_return()
                if left is not None:
                    return left
            if self.has_right():
                right = self._right.find_and_return()
                if right is not None:
                    return right
            return None


    #todo: test
    def set_child(self, node, position):
        if position == 'left':
            self._left = node
            node._parent = self
        elif position == 'right':
            self._right = node
            node._parent = self
        raise RuntimeWarning('Cannot set_child for "root".')

    #todo: test
    def which_child(self):
        if self.is_root():
            return None
        if self.parent()._left is self:
            return 'left'
        else:
            return 'right'

    #todo: test
    def sibling(self):
        if self.is_left():
            return self._parent._right
        elif self.is_right():
            return self._parent._left

    #todo: test
    # swap self and node, that way it should be clearer to read.
    def replace_with(self, child):
        '''
        replaces self with node.
        '''
        if self.is_root():
            child._parent = child
        else:
            if self.is_left():
                self._parent._left = child
            elif self.is_right():
                self._parent._right = child
            child._parent = self._parent
        return self

    #todo: test
    def remove(self):
        '''
        This method should only be called for '!' nodes
        '''
        token = self._parent._token
        parent = self._parent
            #todo: check case, when * is root
        if token in ['*', '!']:
            #todo if parent.is_root():
            parent.remove()
        elif token == '+':
            parent.replace_with(self.sibling())


    # don't use
    def tidy_up(self):
        parent = self._parent
        if self._parent._token == '+':
            grandp = parent._parent
            if parent.is_left() and self.is_left():
                grandp._left = parent._right
                grandp._left._parent = grandp
            elif parent.is_left() and self.is_right():
                grandp._left = parent._left
                grandp._left._parent = grandp
            elif parent.is_right() and self.is_right():
                grandp._right = parent._left
                grandp._right._parent = grandp
            elif parent.is_right() and self.is_left():
                grandp._right = parent._right
                grandp._right._parent = grandp
        else:
            parent.tidy_up()

    def inorder(self):
        '''
        returns a string representation of the tree (going only downwards).
        '''
        term = ''

        if self.has_left() or self.has_right():
            if self.left() is None: # handeling unary operator
                term += '('
            else:
                term += '(' + self._left.inorder()
        term += self._token
        if self.has_right():
            term += self._right.inorder() + ')'
        return term

    def deep_copy(self):
        '''
        copy only subtree, where current Node is root.
        '''
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
                if item == '!':
                    current.tidy_up()
                current = current.new_right()
            elif item == '!':
                current = current._parent
                current._token = item
                current._left = None
                current = current.new_right()
            elif item == '(':
                current = current.new_left()
            elif item == ')':
                current = current._parent
            else:
                current._token = item
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
