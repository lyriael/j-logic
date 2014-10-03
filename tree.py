from node import Node
from helper import parse
from helper import replace
from helper import wild_list
from helper import y_to_x
from helper import unique_wilds
from helper import merge

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
        !! DEPRICATED! -> @mismatch_search -> compare_to

        Wrapper to make handling easier (and correct!)

        Example for return array:

        [('X3', '((a*b):Z)'), ('X2', 'Y')]
        '''
        a = Tree(term_a)
        b = Tree(term_b)
        matches = Tree._possible_match(a.root, b.root)
        x_s = wild_list(term_a)

        if isinstance(matches, list) and len(matches) == len(x_s):
            return matches
        else:
            return False

    @staticmethod
    def _possible_match(node_a, node_b):
        '''
        Wrapper, see possible_match

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
        Wrapper for match_against

        :param term_a: may contain wilds such as X1
        :param term_b: must not contain any wilds, only constants
        :return:
        '''
        mismatch = []
        wilds = []
        if str(node_a) == str(node_b):
            pass
        else:
            result = node_a.compare_to_OLD(node_b)
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
    def match_against(term_a, term_b):
        '''
        ===DEPRECATED===
        see 'compare_to'
        ================
        wrapper for _mismatch_search

        :param term_a: one node of term_a can be a subtree of term_b.
        :param term_b: a subtree of term_b can be matched to one single node of term_a.
        :return wilds:
        List of Tuples, here at first position the collecting node of term_a is, and at second position the
        corresponding subtree of term_b

        Examples:
        term_a = (A->B)->C
        term_b X1->X2
            => [('X1', '(A->B)'), ('X2', 'C')]

        term_a = (X1->X2)->X3
        term_b = Y1->Y2
            => [('Y1', 'X1->X2'), ('Y2', 'X3')]
        '''
        mismatch, wilds = Tree._mismatch_search(Tree(term_a).root, Tree(term_b).root)
        if len(mismatch)>0:
            return False
        else:
            return wilds

    def compare_to(self, other_tree):
        '''
        ===DEPRECATED===
        see 'compare_second_try'
        ================
        This is a wrapper method for the recursive method in Node that compares the tree structure.
        self should be the tree that is less deep than 'other_tree', so that wilds (X's, bzw. Y's) are here.

        :param other_tree:      Tree that contains only X's if self contains Y's.
        :return:
            True,               For exact match.
            False,              No possible match.
            List of tuples,     If there is a wild match (only X's).
        '''
        match, wilds_x, wilds_y = self.root.compare_node_to(other_tree.root, {})
        wilds_x_additionals = y_to_x(wilds_y)
        if match:
            return wilds_x if len(wilds_x) > 0 else True
        else:
            return False

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

    @staticmethod
    def apply_condition(merged: list, condition: tuple):
        '''

        :param merged:
        :param condition:
        :return:
        '''
        index = int(condition[0][1:])-1
        size = len(merged)
        condition_term = condition[1]
        # ################
        # ('X2', '(A->B)')
        # ################
        if 'X' not in condition_term and 'Y' not in condition_term:
            # matches what's already there, or empty
            # print(condition_term)
            # print(merged[index])
            if condition_term == merged[index] or merged[index] == '':
                merged[index] = condition_term
                return merged, True
            else:
                return None, None
        # #################
        # ('X1', '(X2->F)')
        # #################
        if 'X' in condition_term and 'Y' not in condition_term:
            # print(merged[index])
            # if 'X1' != ''
            if merged[index]:
                # compare value of 'X1' with condition_term.
                con, wild = Tree.compare_second_try(Tree(condition_term).root, Tree(merged[index]).root, [], {})
                # print(wild)
                # print(con)
                # assert there are no conditions, check if the wilds fit merged.
                assert con == []
                tmp = list(merged)
                for key in wild:
                    i = int(key[1:])-1
                    if wild[key] == merged[i] or merged[i] == '':
                        tmp[i] = wild[key]
                    else:
                        return None, None
                return tmp, True
            # if 'X1' = ''
            else:
                # see if for all occurring 'Xn' in condition_term are already set.
                xs_in_condition = unique_wilds(condition_term)
                wilds = {}
                tmp = str(condition_term)
                for x in xs_in_condition:
                    i = int(x[1:])-1
                    if merged[i] == '':
                        return merged, False
                    else:
                        tmp = tmp.replace(x, merged[i])
                merged[index] = tmp
                return merged, True
        # ####################
        # if ('X1', '(Y1->F)')
        # ####################
        if 'X' not in condition_term and 'Y' in condition_term:
            # if 'X1' != ''
            if merged[index]:
                # because this method was not intended for what what I'm doing now, here's a little bit of hacking
                # that's doesn't seem to make sense.
                y_to_x_condition_term = str(condition_term.replace('Y', 'X'))
                con, wild = Tree.compare_second_try(Tree(y_to_x_condition_term).root, Tree(merged[index]).root, [], {})
                # print(con)
                # print(wild)
                if wild is None:
                    assert con is None
                    return None, None
                else:
                    assert con == []
                    y_wild ={}
                    for key in wild:
                        y_wild['Y'+key[1:]] = wild[key]
                    return merged, y_wild
            else:
                # if there is no value in 'X1' then 'Y' doesn't matter
                return merged, False
        # ####################
        # if ('X1', '(Y1->F)') !!! THIS SHOULD (HOPEFULLY) NEVER HAPPEN !!!
        # ####################
        if 'X' in condition_term and 'Y' in condition_term:
            print('This should have never happened...')
            assert False

    @staticmethod
    def merge_two_tables(first, second):
        '''
        :param first:
        :param second:
        :return:
        '''
        # todo: may be needs to be moved as well
        # holds all matches
        merged_tables = []
        for tpl in first:
            for candidate_tpl in second:

                simple_merge = merge(tpl[0], candidate_tpl[0])
                conditions = tpl[1] + candidate_tpl[1]

                if simple_merge:
                    # no conditions, yej!
                    if not conditions:
                        merged_tables.append((simple_merge, []))

                    # conditions apply to merge, oh noes..
                    else:
                        todo_conditions = list(conditions)
                        done_conditions = []
                        updated_merge = simple_merge

                        # check every condition
                        while todo_conditions:
                            current = todo_conditions.pop()
                            updated_merge, delete_condition = Tree.apply_condition(updated_merge, current)

                            # merge can fulfills
                            if updated_merge:
                                # condition is fulfilled an no longer needed, also merge was successful.
                                if delete_condition is True:
                                    # condition was already deleted by poping it.
                                    pass
                                # condition does not matter for this merge, but might be needed later.
                                if delete_condition is False:
                                    done_conditions.append(current)
                                # condition could be fulfilled, but other conditions must be updated.
                                elif isinstance(delete_condition, dict):
                                    change_and_todo = get_all_with_y(todo_conditions, delete_condition.keys()) + \
                                                      get_all_with_y(done_conditions, delete_condition.keys())
                                    for key in delete_condition:
                                        change_and_todo = update_y(change_and_todo, key, delete_condition[key])
                                    todo_conditions = todo_conditions + change_and_todo
                            # condition is not compatible with merge
                            if not updated_merge:
                                updated_merge = None
                                break
                        # end of 'while todo_conditions'

                        # All conditions were successful apply
                        if updated_merge:
                            merged_tables.append((updated_merge, done_conditions))
        return merged_tables





def get_all_with_y(conditions, keys):
    '''
    Elements will be removed from list!
    :param conditions:
    :param keys:
    :return:
    '''
    result = []
    for con in conditions[:]:
        # check in con[1] if anything from keys occurrs
        if any(y in con[1] for y in keys):
            conditions.pop()
            result.append(con)
    return result


def update_y(conditions, key, value):
    '''

    :param conditions:
    :param wilds:
    :return:
    '''
    result = []
    for con in conditions:
        if key in con[1]:
            result.append((con[0], con[1].replace(key, value)))
        else:
            result.append((con[0], con[1]))
    return result