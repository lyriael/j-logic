from node import Node
from helper import parse
from helper import replace


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
        return self._inorder_string(self.root)

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

    def preorder_nodes(self, node):
        nodes = [node]
        if node.has_left():
            nodes += self.preorder_nodes(node.left)
        if node.has_right():
            nodes += self.preorder_nodes(node.right)
        return nodes

    def leaves(self, node):
        #todo: test
        leaves = []
        if node.token.alpha():
            leaves.append(node)
        else:
            if node.has_left():
                leaves += self.leaves(node.left)
            if node.has_right():
                leaves += self.leaves(node.right)
        return leaves

    def subtree(self, node):
        term = self._inorder_string(node)
        return Tree(term)

    def deep_copy(self):
        return Tree(self._inorder_string(self.root))

    def first(self, token):
        nodes = self.preorder_nodes(self.root)
        for node in nodes:
            if node.token == token:
                return node
        return None

    def left_split(self, node):
        '''
        Caution: makes direct changes to the tree
        '''
        if node.position == 'root':
            node.left.set_root()
            self.root = node.left
        else:
            node.left.parent = node.parent
            if node.position == 'left':
                node.parent.set_left(node.left)
            elif node.parent == 'right':
                node.parent.set_right(node.left)

    def right_split(self, node):
        '''
        Caution: makes direct changes to the tree
        '''
        if node.position == 'root':
            node.right.set_root()
            self.root = node.right
        else:
            node.right.parent = node.parent
            if node.position == 'left':
                node.parent.set_left(node.right)
            elif node.parent == 'right':
                node.parent.set_right(node.right)

    def has_bad_bang(self):
        '''
        This method expects the formula to be splited and simplified already,
        sucht that only '*', '!' and const are nodes.
        '''
        for node in self.preorder_nodes(self.root):
            if node.token == '!' and node.position == 'left':
                return True
        return False

    def proof_terms(self):
        '''
        This method expects the formula to be splited and simplified already,
        sucht that only '*', '!' and const are nodes.
        '''
        consts = {}
        for leaf in self.leaves(self.root.left):
            consts[leaf.token] = []
        #todo:test
        v_count = 1
        temp = [self]
        while len(temp) > 0:
            f = temp.pop()
            proof_term = f.subtree(f.root.left)
            subformula = f.subtree(f.root.right).to_s()
            if len(proof_term.to_s()) == 1: # constant
                consts[proof_term.to_s()] = subformula
            else:
                if proof_term.root.token == '*':
                    left = proof_term.subtree(f.root.left).to_s()
                    right = proof_term.subtree(f.root.right).to_s()
                    temp.append(Tree('('+left+':(X_'+str(v_count)+'->'+subformula+'))'))
                    temp.append(Tree('('+right+':X_'+str(v_count)+')'))
                    v_count += 1
                elif proof_term.root.token == '!':
                    left = proof_term.subtree(f.root.left).to_s()
                    s = '('+left+':'+str(v_count)+')'
                    temp.append(Tree(s))
                    replace(consts, subformula, s)