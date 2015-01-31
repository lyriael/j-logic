from node import Node


class Tree(object):
    '''
    All searches and changes within a formula.
    '''

    def __init__(self, formula):
        self.root = Node()
        self._parse_formula(formula)

    def __str__(self):
        return self._inorder_string(self.root)

    def __eq__(self, other):
        return str(self) == str(other)

    def _parse_formula(self, formula):
        """
        Makes a binary tree from the given Formula. Used only for initialization.

        :param formula: String
        :return: None
        """
        term = _prepare_parse(formula)
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

    def _inorder_string(self, node):
        '''

        :param node: Node
            Node from where on the inorder should start.
        :return term: string
            Nodes as a String in inorder.
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

    def _preorder_nodes(self, node):
        '''
        Used by different methods to walk the tree.

        :param node: Node
            Node from where the preoder should start.
        :return nodes: list
            All nodes in preoder.
        '''
        nodes = [node]
        if node.has_left():
            nodes += self._preorder_nodes(node.left)
        if node.has_right():
            nodes += self._preorder_nodes(node.right)
        return nodes

    def first(self, token):
        '''
        Find first occurrence of a certain token in the tree using preorder.

        :param token: String
        :return node: Node
        '''
        nodes = self._preorder_nodes(self.root)
        for node in nodes:
            if node.token == token:
                return node
        return None

    def is_wild(self):
        return self.root.is_leaf() and ('X' in self.root.token or 'Y' in self.root.token)

    def _left_split(self, plus_node):
        '''
        Caution: makes direct changes to the tree
        Expects the node to have token '+'
        '''
        if plus_node.position == 'root':
            plus_node.left.set_root()
            self.root = plus_node.left
        else:
            if plus_node.position == 'left':
                plus_node.parent.set_left(plus_node.left)
            elif plus_node.position == 'right':
                plus_node.parent.set_right(plus_node.left)

    def _right_split(self, plus_node):
        '''
        Caution: makes direct changes to the tree
        Expects the node to have token '+'
        '''
        if plus_node.position == 'root':
            plus_node.right.set_root()
            self.root = plus_node.right
        else:
            if plus_node.position == 'left':
                plus_node.parent.set_left(plus_node.right)
            elif plus_node.position == 'right':
                plus_node.parent.set_right(plus_node.right)


def subtree(node):
    '''
    Returns a deep copy of the subtree of the given node.

    :param node: Node
    :return subtree: Tree
    '''
    if node is None:
        return Tree('')
    else:
        return Tree(str(node))


def _prepare_parse(string):
    '''
    separate operators, parentheses and variables and returns them as a list.
    '''
    l = list(string)
    for index in range(len(l)):
        if l[index].isdigit():
            l[index] = l[index-1] + l[index]
            l[index-1] = ''

        if l[index] == '>':
            assert l[index-1] == '-'
            l[index] = l[index-1] + l[index]
            l[index-1] = ''
    while '' in l:
        l.remove('')
    return l