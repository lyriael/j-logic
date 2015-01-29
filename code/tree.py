from node import Node
from collections import defaultdict
import itertools


class Tree(object):
    '''
    All searches and changes within a formula.
    '''

    def __init__(self, formula):
        self.root = Node()
        self._parse_formula(formula)

    def _parse_formula(self, formula):
        """
        Makes a binary tree from the given Formula. Used only for initialization.

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

    def _preorder_nodes(self, node):
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

    #todo: make static
    def subtree(self, node):
        '''
        Returns a deep copy from the subtree of the given node.

        :param node:
        :return subtree: Tree
        '''
        if node is None:
            return None
        else:
            return Tree(self._inorder_string(node))

    def deep_copy(self):
        return Tree(self._inorder_string(self.root))

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

    @staticmethod
    def musts(formula: str):
        '''
        This method expects the formula to be splited and simplified already,
        such that only '*', '!' and const are nodes.

        It returns a List with tuples, where the first entry is the proof constant
        and the second the other part (thingy after ':'...).

        THE MAGIC HAPPENS RIGHT HERE
        '''
        tree = Tree(formula)
        consts = []         # returning container.
        swaps = []          # contains replacements for Wilds from '!'. => ('X2', '(b:X3)')
        v_count = 1         # needed for Wilds (X1, X2, ...)
        temp = [tree]  # contains Trees
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

    @staticmethod
    def sum_split(formula):
        '''
        Transforms formula to a disjunctive form.
        algorithm:

        search for first '+'
            if there is none you're done.
            if there is one, split the formula and repeat the step above for both parts.

        :return: list
            formulas as Strings.

        Example:
        ((a+b):F) => ['(a:F)', '(b:F')]

        Remark:
        If no sum exists in the formula, the returned list will simply contain the original formula.
        A empty List should never be returned.
        '''
        tree = Tree(formula)
        proof_term = tree.subtree(tree.root.left)   # Tree, e.g.: ((a*b)+c)
        subformula = tree.root.right.to_s()         # String, e.g.: F

        done = []
        todo = [proof_term]
        while len(todo) > 0:
            f = todo.pop()
            if f.first('+') is None:
                done.append(f)
            else:
                left = f.deep_copy()
                node = left.first('+')
                left._left_split(node)
                todo.append(left)

                right = f.deep_copy()
                node = right.first('+')
                right._right_split(node)
                todo.append(right)

        # make to string and remove duplicates
        result = []
        for tree in done:
            result.append('('+tree.to_s()+':'+subformula+')')
        return list(set(result))

    @staticmethod
    def simplify_bang(formula):
        '''
        Called from ProofSearch in step 'atomize'. Simplifies a formula for top '!' operations.

        Example:
        (a:F)         => (a:F)
        ((!a):(a:F))  => (a:F)
        ((!b):F)      => None

        :return str:
            old Formula,    if '!' is not top operation
            new Formula,    if resolvable
            empty,          if not resolvable
        '''
        tree = Tree(formula)
        assert tree.root.token == ':'

        if tree.root.left.token == '!':
            # accessing child of '!'
            left = tree.subtree(tree.root.left.right)
            right = tree.subtree(tree.root.right.left)
            # if both sides are the same, construct simplified formula as string.
            if right and left.to_s() == right.to_s():
                subformula = tree.subtree(tree.root.right.right)
                s = '('+right.to_s()+':'+subformula.to_s()+')'
                return s
            else:
                return ''
        else:
            # formula has no '!' operation on top.
            return formula

    @staticmethod
    def has_bad_bang(formula):
        '''
        Checks if there is a left '!' of '*' somewhere in the Formula.

        restriction: Must only be called on a Formula where top operation is ':'.

        :return boolean:
            True, if a left '!' of '*' is found somewhere in the tree.
            False, else.
        '''
        tree = Tree(formula)
        proof_term_tree = Tree(tree.root.left.to_s())
        assert tree.root.token == ':'
        for node in proof_term_tree._preorder_nodes(tree.root):
            if node.token == '!' and node.position == 'left':
                return True
        return False


def unify(f1, f2):
    '''

    :param f1: string
    :param f2: string
    :return: dict
    '''
    stack = [(Tree(f1), Tree(f2))]
    result = []
    while len(stack) > 0:
        current = stack.pop()
        # If the root node is the same (either operation or constant)
        if current[0].root.token == current[1].root.token:
            if current[0].root.token in ['->', ':']:
                stack.append((current[0].subtree(current[0].root.left), current[1].subtree(current[1].root.left)))
                stack.append((current[0].subtree(current[0].root.right), current[1].subtree(current[1].root.right)))
            else:
                pass
        # If the root is not the same, either it is a mismatch, or there are wilds.
        # Stuff that is put in 'result' has on one side only a wild-constant.
        else:
            # (X1, A->B), (Y1, G), ...
            if (has_no_wilds(current[0].to_s()) and has_wilds(current[1].root.token)) or \
                (has_no_wilds(current[1].to_s()) and has_wilds(current[0].root.token)):
                result.append((current[0].to_s(), current[1].to_s()))
            # (X1, Y2->F), (Y1, X1), (X1, Y1->Y1), ...
            elif has_wilds(current[0].to_s()) and has_wilds(current[1].to_s()):
                assert has_wilds(current[0].root.token) or has_wilds(current[1].root.token)
                result.append((current[0].to_s(), current[1].to_s()))
            # (Y1->F, b:B), (F, Y1->Y2), ...
            else:
                return None

    return condition_list_to_dict(result)


def condition_list_to_dict(conditions):
    '''

    :param conditions: list of tuples
    :return: dict
    '''
    dct = defaultdict(list)
    if not conditions:
        return {}

    # breaking tuples up and sort the values into a dict.
    for con in conditions:
        if con[0][0] in ['Y', 'X']:
            dct[con[0]].append(con[1])
        if con[1][0] in ['Y', 'X']:
            dct[con[1]].append(con[0])

    # adding all variables to the dic, even if they are not isolated and
    for key in dct:
        dct[key] = list(set(dct[key]))

    return dct


def condition_dict_to_list(conditions):
    '''

    :param conditions: dict
    :return: list of tuples
    '''
    lst = []
    if not conditions:
        return []

    for key in conditions:
        for item in conditions[key]:
            lst.append((key, item))
    return list(set(lst))

def simplify(var, conditions):
    '''

    :param var: string
    :param conditions: dict
    :return: dict
    '''

    # get all (X1, F)
    fs = conditions.pop(var, [])

    # if there are no conditions for var, we're done.
    if not fs:
        conditions[var] = []
        return conditions

    # preprocess those, if there is any condition where X1 occures in Fi, then we have a contradiction.
    for fi in fs:
        if var in fi and var != fi:
            return None

    # unify, gives new conditions. If any match returns None, we have a contradiction and stop.
    a_lst = []
    for f1, f2 in itertools.combinations(fs, 2):
        new_conditions = unify(f1, f2)
        if new_conditions is None:
            return None
        a_lst += condition_dict_to_list(new_conditions)
    a_dct = condition_list_to_dict(a_lst)

    # keep one of the (X1, Fi)
    chosen = fs.pop()

    # replace all X1 in rest
    for key in conditions:
        tmp = []
        for item in conditions[key]:
            tmp.append(item.replace(var, chosen))
        conditions[key] = tmp

    # add new conditions to old conditions and collect new variables
    new_vars = []
    for key in a_dct:
        if not conditions[key]:
            new_vars.append(key)
        conditions[key] += a_dct[key]
        conditions[key] = list(set(conditions[key]))

    # add the chosen one
    conditions[var] = [chosen]

    return new_vars


def resolve_conditions(conditions):
    '''
    :param conditions: dict
    :return: dict
    '''

    vars_todo = list(conditions.keys())
    # so a simplify for all vars
    while len(vars_todo) > 0:
        var = vars_todo.pop()
        new_vars = simplify(var, conditions)
        if new_vars is None:
            return None
        vars_todo += new_vars
    return conditions

def parse(string):
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


def has_no_wilds(term):
    return not ('X' in term or 'Y' in term)


def has_wilds(term):
    return 'X' in term or 'Y' in term


def replace(consts, swaps):
    '''
    :param:
    swaps: [('X2', '(b:X3)'), ...]
    Wilds that must be replaces because of '!'

    consts: [('a', ['(X2->(X1->F))]), ...]

    :return:
    adjusted const => [('a', ['((b:X3)->(X1->F))]), ...]
    '''
    new_consts = []
    for term in consts:
        tmp = term[1]
        for replacement in swaps:
           tmp = tmp.replace(replacement[0], replacement[1])
        new_consts.append((term[0], tmp))
    return new_consts