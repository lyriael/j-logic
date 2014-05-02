class Node(object):

    def __init__(self):
        self.token = 'no token'
        self.parent = self
        self.left = None
        self.right = None

    def __repr__(self):
        return self.token

    def is_root(self):
        return self.parent is self

    def is_leaf(self):
        return self.left is None and self.right is None

    def has_left(self):
        return self.left is not None

    def has_right(self):
        return self.right is not None

    def get_right(self):
        return self.right

    def get_left(self):
        return self.left

    def new_left(self):
        new_left = Node()
        self.left = new_left
        new_left.parent = self
        return new_left

    def new_right(self):
        new_right = Node()
        self.right = new_right
        new_right.parent = self
        return new_right

    # todo: needs to be fixed. Parentheses for ! and return string, rather than direct printing.
    def preorder(self):
        print(self)
        if self.left:
            self.left.preorder()
        if self.right:
            self.right.preorder()

    def inorder(self):
        term = ''
        if self.has_left():
            term += '(' + self.left.inorder()
        term += str(self)
        if self.has_right():
            term += self.right.inorder() + ')'

        if self.token == '!':
            term = term[:-1]
        return term

    @staticmethod
    def make_tree(term):
        root = Node()
        current = root
        for i in term:
            if i in ['(', ')', '+', '!', ':']:
                if i == '(':
                    left = current.new_left()
                    current = left
                if i == ')':
                    current = current.parent
                if i == '+':
                    current.token = '+'
                    right = current.new_right()
                    current = right
                if i == ':':
                    current.token = ':'
                    right = current.new_right()
                    current = right
                if i == '!':
                    current.token = '!'
                    only = current.new_right()
                    current = only
            else:
                current.token = i
                if current.parent.token == '!':
                    current = current.parent.parent
                else:
                    current = current.parent
        return root



# tests = ['(c+(a+b))', '!a']
# tree_root = Node.make_tree('((c+(a+b)):A)')
#
#
# print("INORDER")
# print(tree_root.inorder())
# print("PREORDER")
# print(root.preorder())
# print("SIZE")
# print(len(tree))
# for i in Node.make('(c+(a+b)):C'):
#     print("looking at: " + i.token)
#     print("left: " + str(i.has_left()))
#     print("right: " + str(i.has_right()))
#     print("root: " + str(i.is_root()))
#     print("leaf: " + str(i.is_leaf()))
#     print("-----------------------")
