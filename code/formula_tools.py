from tree import Tree
from collections import defaultdict
import itertools


def sum_split(formula):
    '''
    Transforms formula to a disjunctive form.
    algorithm:

    search for first '+'
        if there is none you're done.
        if there is one, split the formula and repeat the step above for both parts.

    Example:
    ((a+b):F) => ['(a:F)', '(b:F')]

    Remark:
    If no sum exists in the formula, the returned list will simply contain the original formula.
    A empty List should never be returned.

    :return formulas: list
    '''
    tree = Tree(formula)
    proof_term = tree.subtree(tree.root.left)   # Tree, e.g.: ((a*b)+c)
    subformula = tree.root.right.to_s()         # String, e.g.: F

    done = []
    todo = [proof_term]
    while todo:
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
        result.append('(%s:%s)' % (str(tree), subformula))
    return list(set(result))


def simplify_introspection(formula):
    '''
    Called from ProofSearch in step 'atomize'. Simplifies a formula for top '!' operations.

    Example:
    (a:F)         => (a:F)
    ((!a):(a:F))  => (a:F)
    ((!b):F)      => None

    :return formula: str
    '''
    tree = Tree(formula)
    assert tree.root.token == ':'

    if tree.root.left.token != '!':
        # formula has no '!' operation on top.
        return formula
    else:
        # Comparing subtrees
        #        :
        #      /   \
        #     !    ST
        #      \
        #      ST
        left = tree.subtree(tree.root.left.right)
        right = tree.subtree(tree.root.right.left)
        # if both sides are the same, construct simplified formula as string.
        if right == left:
            subformula = tree.subtree(tree.root.right.right)
            return '(%s:%s)' % (str(right), str(subformula))
        else:
            return None


def has_bad_introspection(formula):
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


def musts(proof_term):
    '''
    This method will retrieve all proof constants with their corresponding formulas derived from the proof term.

    :param proof_term: string
        The formula is expected to be already atomized such that only *, ! and proof constants are nodes.
    :return musts: list
        List of tuples, where the first entry is the proof constant and the second part is a term, usually containing
        variables (X-wilds).
    '''
    tree = Tree(proof_term)
    consts = []         # returning container. Formulas in string form.
    swaps = []          # contains replacements for Wilds from '!'. => ('X2', '(b:X3)') in string form
    v_count = 1         # needed for Wilds (X1, X2, ...)
    todo = [tree]       # contains trees that still need to be handled.
    while todo:
        f = todo.pop()
        proof_term = f.subtree(f.root.left)
        subformula = f.subtree(f.root.right)

        if proof_term.root.is_leaf(): # constant
            consts.append((str(proof_term), str(subformula)))
        elif proof_term.root.token == '*':
            left = proof_term.subtree(proof_term.root.left)
            right = proof_term.subtree(proof_term.root.right)
            todo.append(Tree('(%s:(X%s->%s))' % (str(left), str(v_count), str(subformula))))
            todo.append(Tree('(%s:X%s)' % (str(right), str(v_count))))
            v_count += 1
        elif proof_term.root.token == '!':
            left = proof_term.subtree(f.root.left.right)
            s = '(%s:X%s)' % (str(left), str(v_count))
            todo.append(Tree(s))
            swaps.append((str(subformula), s))
            v_count += 1
    return sorted(_replace(consts, swaps))


def _replace(consts, swaps):
    '''
    :param consts: list
    :param swaps: list

    Wilds that must be replaces because of '!'. Change are made in place.

    Example:
        swaps: [('X2', '(b:X3)'), ...]
        consts: [('a', ['(X2->(X1->F))]), ...]
        consts: [('a', ['((b:X3)->(X1->F))]), ...]

    :return consts: list
    '''
    for index in range(len(consts)):
        for xi, replacement in swaps:
            consts[index] = (consts[index][0], consts[index][1].replace(xi, replacement))
    return consts


def unify(first_formula, second_formula):
    '''
    This method compares two formulas by matching them against each other. If a match is not possible, None will be
    returned.
    This method makes no further analysis of the matches. Duplicated entries as well as contradiction for one variable
    is possible.

    :param first_formula: string
        First formula.
    :param second_formula: string
        Second formula.
    :return conditions: dict
        The conditions are sorted by variables (X-wilds and Y-wilds). It may be possible that not every variable is
        available as key,  example: {'X2': ['Y1']}.
    '''
    stack = [(Tree(first_formula), Tree(second_formula))]
    result = []
    while stack:
        f1, f2 = stack.pop()
        # If the root node is the same (either operation or constant)
        if f1.root.token == f2.root.token:
            # If the its a operator, go on. If it's a constant we're done.
            if f1.root.token in ['->', ':']:
                stack.append((f1.subtree(f1.root.left), f2.subtree(f2.root.left)))
                stack.append((f1.subtree(f1.root.right), f2.subtree(f2.root.right)))
        # If the root is not the same, either it is a mismatch, or there are wilds.
        # Stuff that is put in 'result' has on one side only a wild-constant.
        else:
            # (X1, A->B), (Y1, G), ...
            if (_has_no_wilds(str(f1)) and _has_wilds(f2.root.token)) or \
                (_has_no_wilds(str(f2)) and _has_wilds(f1.root.token)):
                result.append((str(f1), str(f2)))
            # (X1, Y2->F), (Y1, X1), (X1, Y1->Y1), ...
            elif _has_wilds(str(f1)) and _has_wilds(str(f2)):
                assert _has_wilds(f1.root.token) or _has_wilds(f2.root.token)
                result.append((str(f1), str(f2)))
            # (Y1->F, b:B), (F, Y1->Y2), ...
            else:
                return None
    return condition_list_to_dict(result)


def _has_wilds(term):
    return 'X' in term or 'Y' in term


def _has_no_wilds(term):
    return not _has_wilds(term)


def simplify(var, conditions):
    '''
    This methods resolves the conditions for one variable. By doing so it may happen that new variables are found as
    keys because they were only within a condition before but not a key. For that reason and because this information
    is used later on in the method 'resolve_conditions', those new found variables are returned and not the conditions.

    The conditions will be changed inplace!

    :param var: string
        Variable (X-wild or Y-wild) used as key.
    :param conditions: dict
        All conditions, they will be changed inplace.
    :return new_vars: dict
        New variables that were not present as key before.
    '''
    # get all (X1, Fi)
    fs = conditions.pop(var, [])

    # If there are no conditions for var, we're done.
    if not fs:
        conditions[var] = []
        return conditions

    # Preprocess those: if there is any condition where X1 occurs in Fi, then we have a contradiction,
    # except if X1 == Fi
    for fi in fs:
        if var in fi and var != fi:
            return None

    # Unify each with another: Gives new conditions. If any match returns None, we have a contradiction and stop.
    a_lst = []
    for f1, f2 in itertools.combinations(fs, 2):
        new_conditions = unify(f1, f2)
        if new_conditions is None:
            return None
        a_lst += condition_dict_to_list(new_conditions)
    a_dct = condition_list_to_dict(a_lst)

    # Keep one of the (X1, Fi), so we don't loose all reference.
    chosen = fs.pop()

    # Replace all X1 in the Fis of the other Variables. X1 will only occur as the chosen one.
    for key in conditions:
        tmp = []
        for item in conditions[key]:
            tmp.append(item.replace(var, chosen))
        conditions[key] = tmp

    # Add new conditions to old conditions. Collect new variables to return.
    new_vars = []
    for key in a_dct:
        if not conditions[key]:
            new_vars.append(key)
        conditions[key] += a_dct[key]
        conditions[key] = list(set(conditions[key]))

    # Finally add the chosen one to the conditions.
    conditions[var] = [chosen]
    return new_vars


def condition_list_to_dict(conditions):
    '''
    Converts a condition list into a condition dictionary.

    :param conditions: list
        A list of tuples, where the first place within the tuple is a single variable (X-wild or Y-wild) and the other
        term is a condition that applies to that variable.
    :return: dict
        In the dictionary the conditions are sorted by variable (X-wilds and Y-wilds) which serve as keys. The
        conditions are in form of a list.
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
    Converts a condition dictionary into a condition list.

    :param conditions: dict
        In the dictionary the conditions are sorted by variable (X-wilds and Y-wilds) which serve as keys. The
        conditions are in form of a list.
    :return: list
        A list of tuples, where the first place within the tuple is a single variable (X-wild or Y-wild) and the other
        term is a condition that applies to that variable.
    '''
    lst = []
    if not conditions:
        return []

    for key in conditions:
        for item in conditions[key]:
            lst.append((key, item))
    return list(set(lst))


def resolve_conditions(conditions):
    '''
    This method takes all conditions and valuates them. It tries to resolve missing variables (X-wilds and Y-wilds)
    and checks if there are any contradictions.

    This method makes inplace changes to the conditions!

    :param conditions: dict
        Variables are keys to their conditions.
    :return conditions: dict
        Resolved conditions, or None if a contradiction is found.
    '''
    vars_todo = list(conditions.keys())
    while vars_todo:
        var = vars_todo.pop()
        new_vars = simplify(var, conditions)
        if new_vars is None:
            return None
        vars_todo += new_vars
    return conditions