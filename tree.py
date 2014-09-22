from node import Node
from helper import parse
from helper import replace
from helper import wilds


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

    def first(self, token):
        nodes = self.preorder_nodes(self.root)
        for node in nodes:
            if node.token == token:
                return node
        return None

    def leaves(self, node):
        leaves = []
        if node.token.isalpha():
            leaves.append(node)
        else:
            if node.has_left():
                leaves += self.leaves(node.left)
            if node.has_right():
                leaves += self.leaves(node.right)
        return leaves

    def subtree(self, node):
        if node is None:
            return None
        else:
            return Tree(self._inorder_string(node))

    def deep_copy(self):
        return Tree(self._inorder_string(self.root))

    def left_split(self, plus_node):
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

    def right_split(self, plus_node):
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

    def has_bad_bang(self):
        '''
        This method expects the formula to be splited and simplified already,
        sucht that only '*', '!' and const are nodes.
        '''
        for node in self.preorder_nodes(self.root):
            if node.token == '!' and node.position == 'left':
                return True
        return False

    def musts(self):
        '''
        This method expects the formula to be splited and simplified already,
        such that only '*', '!' and const are nodes.

        It returns a List with tuples, where the first entry is the proof constant
        and the second the other part (thingy after ':'...).

        THE MAGIC HAPPENS RIGHT HERE
        '''
        consts = []     # returning container.
        swaps = []      # contains replacements for Wilds from '!'. => ('X2', '(b:X3)')
        v_count = 1     # needed for Wilds (X1, X2, ...)
        temp = [self]   # contains Trees
        while len(temp) > 0:
            f = temp.pop()
            proof_term = f.subtree(f.root.left)
            subformula = f.subtree(f.root.right).to_s()

            if len(proof_term.to_s()) == 1: # constant
                consts.append((proof_term.to_s(), subformula))
            else:
                if proof_term.root.token == '*':
                    left = proof_term.subtree(proof_term.root.left).to_s()
                    right = proof_term.subtree(proof_term.root.right).to_s()
                    temp.append(Tree('('+left+':(X'+str(v_count)+'->'+subformula+'))'))
                    temp.append(Tree('('+right+':X'+str(v_count)+')'))
                    v_count += 1
                elif proof_term.root.token == '!':
                    left = proof_term.subtree(f.root.left.right).to_s()
                    s = '('+left+':X'+str(v_count)+')'
                    temp.append(Tree(s))
                    swaps.append((subformula, s))
                    v_count += 1
        return sorted(replace(consts, swaps))

    @staticmethod
    def possible_match(term_a, term_b):
        '''
        !! DEPRICATED! -> @mismatch_search

        Wrapper to make handling easier (and correct!)

        Example for return array:

        [('X3', '((a*b):Z)'), ('X2', 'Y')]
        '''
        a = Tree(term_a)
        b = Tree(term_b)
        matches = Tree._possible_match(a.root, b.root)
        x_s = wilds(term_a)

        if isinstance(matches, list) and len(matches) == len(x_s):
            return matches
        else:
            return False

    @staticmethod
    def _possible_match(node_a, node_b):
        '''
        Returns array that contains wild char matches if the trees match and
        returns False, if there is a mismatch.

        !Only node_a should contain any wildchars (Xs)
        '''
        wilds = []

        # match
        if node_a.token == node_b.token:
            # recursion if both have sons
            if node_a.has_left() and node_b.has_left():
                match = Tree._possible_match(node_a.left, node_b.left)
                if match:
                    wilds += match
            elif node_a.has_left() or node_b.has_left():
                return False

            if node_a.has_right() and node_b.has_right():
                match = Tree._possible_match(node_a.right, node_b.right)
                if match:
                    wilds += match
            elif node_a.has_right() or node_b.has_right():
                return False

        # wild char match
        elif node_a.token[0] == 'X':
            wilds.append((node_a.token, node_b.to_s()))

        # no match at all
        else:
            return False
        return wilds

    @staticmethod
    def _mismatch_search(node_a, node_b):
        '''

        :param term_a: may contain wilds such as X1
        :param term_b: must not contain any wilds, only constants
        :return:
        '''
        mismatch = []
        wilds = []
        if str(node_a) == str(node_b):
            print('should be here')
            pass
        else:
            result = node_a.compare_to(node_b)
            if result == 'no match':
                mismatch.append(True)
            elif result == 'wild match':
                wilds.append((node_a.token, node_b.to_s()))
            # call recursion
            elif result == 'exact match':
                if node_a.has_left() and node_b.has_left():
                    mismatch_tmp, wilds_tmp = Tree._mismatch_search(node_a.left, node_b.left)
                    wilds += wilds_tmp
                    mismatch += mismatch_tmp
                elif node_a.has_left() or node_b.has_left():
                    mismatch.append(True)
                else:
                    # neither has left son
                    pass

                if node_a.has_right() and node_b.has_right():
                    mismatch_tmp, wilds_tmp = Tree._mismatch_search(node_a.right, node_b.right)
                    wilds += wilds_tmp
                    mismatch += mismatch_tmp
                elif node_a.has_right() or node_b.has_right():
                    mismatch.append(True)
                else:
                    # neither has a right son
                    pass
        return mismatch, wilds

    @staticmethod
    def mismatch_search(term_a, term_b):
        '''
        wrapper for _mismatch_search

        :param term_a:
        :param term_b:
        :return:
        '''
        mismatch, wilds = Tree._mismatch_search(Tree(term_a).root, Tree(term_b).root)
        if len(mismatch)>0:
            return False
        else:
            return wilds