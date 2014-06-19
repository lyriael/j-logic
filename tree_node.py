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

    def has_parent(self):
        return self._parent is not None and self._parent is not self

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

    #todo: test
    def sibling(self):
        if self.is_left():
            return self._parent._right
        elif self.is_right():
            return self._parent._left

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

    def remove_bangs(self, current_node):
        '''
        should remove all '!' that occure on left side of '*'
        '''
        #todo:
        if current_node.token() == '!':
            self.remove(current_node)
        if current_node.token() == '+':
            self.remove_bangs(current_node.left())
            self.remove_bangs(current_node.right())
        if current_node.token() == '*':
            self.remove_bangs(current_node.left())
            #todo: hack, find nicer solution. Poblem: if tree or part of it gets deleted.
            if current_node.right() is not None and current_node.right().token() == '*':
                self.remove_bangs(current_node.right())

    def remove(self, node):
        '''
        intended for left subtree of '*' only where node is '!'.
        '''
        if node.is_root():
            self.fell()
            return
        if node.parent().token() == '+':
            self._replace(node.parent(), node.sibling())
        if node.parent().token() == '*':
            self.remove(node.parent())

    def _replace(self, node1, node2):
        '''
        replaces node1 by node2 (ink. subtree).
        It expects that node1 is '+' and a child of '*'.
        '''
        if node1.is_left():
            node1.parent()._left = node2
        elif node1.is_right():
            node1.parent()._right = node2
        node2._parent = node1.parent()

    def fell(self):
        self._left = None
        self._right = None
        self._parent = None
        self._token = ''

    def collect_nodes(self, node):
        '''
        Returns an array that contains all nodes with operation type '+' or '!'.

        Recursive!
        '''
        #todo: is it better to just return one instead of an array?
        nodes = []
        if node.token() in ['+', '!']:
            nodes.append(node)
        if node.has_left():
            nodes += self.collect_nodes(node.left())
        if node.has_right():
            nodes += self.collect_nodes(node.right())
        return nodes

    def get_left_split(self):
        f1 = self.deep_copy()
        print(str(f1.is_root()))
        f1._parent._left = f1.left()
        f1._left._parent = f1.parent()
        print(str(f1))
        return f1

    def get_right_split(self):
        f2 = self.deep_copy()
        f2._parent._right = f2.right()
        f2._right._parent = f2.parent()
        return f2

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

    @staticmethod
    def make_tree_extended(term):
        term = parse(term)
        root = Node()
        current = root

        for item in term:
            if item in [':', '+', '*', '->']:
                current._token = item
                #todo: delete invalid subtree
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
