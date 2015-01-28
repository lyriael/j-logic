from re import findall
from collections import defaultdict
from tree import unify
import itertools


def get_all_wilds(conditions):
    '''

    :param conditions: List of conditions in form of tuples.
    :return: A list containg all variables (X-wilds and Y-wilds).
    '''
    vars = []
    for condition_tuple in conditions:
        vars += findall(r'X\d+|Y\d+', condition_tuple[0])
        vars += findall(r'X\d+|Y\d+', condition_tuple[1])

    return sorted(list(set(vars)))


def group_by_var(conditions):
    '''

    :param conditions: list
    :return: dict
    '''
    dct = defaultdict(list)
    vars = get_all_wilds(conditions)

    # adding all variables to the dic, even if they are not isolated
    for x in vars:
        dct[x]

    # breaking tuples up and sort the values into a dict.
    for con in conditions:
        if con[0][0] in ['Y', 'X']:
            dct[con[0]].append(con[1])
        if con[1][0] in ['Y', 'X']:
            dct[con[1]].append(con[0])
    return dct


def simplify(var, conditions):
    '''

    :param var: string
    :param conditions: dict
    :return:
    '''

    # get all (X1, F)
    fs = conditions.pop(var, None)

    # preprocess those
    fs[:] = [x for x in fs if not var in x]

    # unify, gives new conditions
    a = []
    for f1, f2 in itertools.combinations(fs, 2):
        a += unify(f1, f2)
    a = list(set(a))

    # keep one of the (X1, Fi)
    chosen = fs.pop()

    # replace all X1 in rest
    for key in conditions:
        tmp = []
        for item in conditions[key]:
            tmp.append(item.replace(var, chosen))
        conditions[key] = tmp

    # add new conditions to old conditions
    dic_a = group_by_var(a)
    for key in dic_a:
        conditions[key] += dic_a[key]
        conditions[key] = list(set(conditions[key]))
    # add the chosen one
    conditions[var] = [chosen]

    return tuple((var, chosen))


def resolve_conditions(conditions):
    '''

    :param conditions: list
    :return:
    '''

    dict_conditions = group_by_var(conditions)
    variables = dict_conditions.keys()

    for x in variables:
        simplify(x, dict_conditions)

    return dict_conditions

