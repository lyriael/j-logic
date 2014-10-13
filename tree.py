from node import Node
from helper import parse
from helper import replace
from helper import unique_wilds
from helper import merge


class Tree(object):
    '''
    All searches and changes within a formula.
    '''

    def __init__(self, formula):
        self.root = Node()
        self._parse_formula(formula)

    def _parse_formula(self, formula):
        """
        Makes a binary tree from the given Formula.

        :param formula: String
        :return: None
        """
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
    def compare_second_try(orig_node, cs_node, conditions, wilds):
        '''
        from 2.10.14
        changes the tree while comparing.
        self == x (orig)
        mutable == y/const (cs)

        :param mutable:
        :return:
        '''
        # todo: rename this method!!
        # if current node is Yn, then replace all occurring Yn's with whatever is in orig.
        if cs_node.token[0] == 'Y':
            Tree._replace_in_tree(cs_node.get_root(), cs_node.token, Tree(orig_node.to_s()).root)
            #todo: maybe there is replacement needed in conditions as well.
        # if current node is Xn, then this is the consequence of a Yn being replaced. What
        # ever is in orig is a condition to Xn.
        elif cs_node.token[0] == 'X':
            # condition
            if 'X' in orig_node.to_s():
                t = (cs_node.token, orig_node.to_s())
                conditions.append(t)
            # wild
            else:
                wilds[cs_node.token] = orig_node.to_s()
        # unresolved 'Y' in cs-subtree to corresponding 'X' in orig => condition
        elif orig_node.token[0] == 'X' and ('Y' in cs_node.to_s() or 'X' in cs_node.to_s()):
            t = (orig_node.token, cs_node.to_s())
            conditions.append(t)
        # normal wild config
        # todo: OMG, what shall be done, if there is a Y inside??!!
        # todo: check if a X in wilds can be overwritten by accident
        elif orig_node.token[0] == 'X':
            wilds[orig_node.to_s()] = cs_node.to_s()
        # if both are same
        elif orig_node.token == cs_node.token:
            if orig_node.token in ['->', ':']:
                conditions, wilds = Tree.compare_second_try(orig_node.left, cs_node.left, conditions, wilds)
                conditions, wilds = Tree.compare_second_try(orig_node.right, cs_node.right, conditions, wilds)
            else:
                # same constant
                pass
        else:
            # no match possible
            # no idea how to make that nicer
            conditions, wilds = None, None
        return conditions, wilds

    @staticmethod
    def _replace_in_tree(current_node: Node, old: str, replacement: Node):
        '''
        used in compare_second_try
        :param old_node:
        :param replacement:
        :return:
        '''
        if current_node.token == old:
            current_node.swap_with(replacement)
        else:
            if current_node.has_left():
                Tree._replace_in_tree(current_node.left, old, replacement)
            if current_node.has_right():
                Tree._replace_in_tree(current_node.right, old, replacement)

    def _sum_split(self):
        '''
        Transforms formula to a disjunctive form.
        algorithm:

        search for first '+'
            if there is none you're done.
            if there is one, split the formula and repeat the step above for both parts.

        :return:
        List of Formulas.

        Example:
        ((a+b):F) => [a:F, b:F]

        Remark:
        If no sum exists in the formula, the returned list will simply contain the same formula.
        A empty List should never be returned.
        '''
        proof_term = self.subtree(self.root.left) # Formula
        subformula = self.subtree(self.root.right).to_s() # String
        done = []
        todo = [proof_term]
        while len(todo) > 0:
            f = todo.pop()
            if f.first('+') is None:
                done.append(f)
            else:
                left = f.deep_copy()
                node = left.first('+')
                left.left_split(node)
                todo.append(left)

                right = f.deep_copy()
                node = right.first('+')
                right.right_split(node)
                todo.append(right)
        # make to string and remove duplicates
        temp = []
        for tree in done:
            temp.append('('+tree.to_s()+':'+subformula+')')
        temp = list(set(temp))
        # make to Formulas
        formulas = []
        for s in temp:
            formulas.append(Tree(s))
        return formulas

    def _simplify_bang(self):
        '''
        Simplify Formula by resolving top '!'.

        restriction:
        - Must only be called on a Formula where top operation is ':' and to left operation is '!'.

        :return:
        new Formula,    if resolvable
        None,           if not resolvable

        Example:
        ((!(a)):(a:F))  => (a:F)
        ((!(b)):F)      => None
        '''
        # accessing child of '!'
        left = self.subtree(self.root.left.right)
        right = self.subtree(self.root.right.left)
        if right and left.to_s() == right.to_s():
            subformula = self.subtree(self.root.right.right)
            s = '('+right.to_s()+':'+subformula.to_s()+')'
            return Tree(s)
        else:
            return None

    def _has_bad_bang(self):
        '''
        Checks if there is a left '!' of '*' somewhere in the Formula.

        restriction:
        - Must only be called on a Formula where top operation is ':'.
        :return:
        '''
        proof_term_tree = Tree(self.root.left.to_s())
        if proof_term_tree.has_bad_bang():
            return True
        else:
            return False


