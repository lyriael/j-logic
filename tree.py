class Node(object):

    def __init__(self):
        self.token = 'no token'
        self.parent = None
        self.left = None
        self.right = None

    def __repr__(self):
        return self.token

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return self.left is None and self.right is None

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

    def preorder(self):
        print(self)
        if self.left:
            self.left.preorder()
        if self.right:
            self.right.preorder()


def make(term):
    current = Node()
    all = [current]
    j = 0   # for debugging
    for i in term:
        if i in ['(', ')', '+']:
            if i == '(':
                left = current.new_left()
                current = left
                all.append(current)
            if i == ')':
                current = current.parent
            if i == '+':
                current.token = '+'
                right = current.new_right()
                current = right
                all.append(current)
        else:
            current.token = i
            current = current.parent
        j += 1

    return all


r = make('(c+(a+b))')
r[0].preorder()
print(r)
