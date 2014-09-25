from re import findall

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


def size(musts):
    '''
    Takes an list of tuples as input and
    searches for to highest occurring X..
    '''
    all_xs = []
    for term in musts:
        all_xs += wilds(term[1])
    all_xs = sorted(list(set(all_xs)))
    return sorted(map(lambda x: int(x[1:]), all_xs)).pop()

def merge(a, b):
    '''
    compares to lists, if they are mergable return the merge, else return None.
    '''
    s = len(a)
    m = ['']*s
    for i in range(s):
        if a[i] == b[i]:
            m[i] = a[i]
        elif a[i] == '':
            m[i] = b[i]
        elif b[i] == '':
            m[i] = a[i]
        else:
            return None
    return m

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


def config_dict(term, size):
    return init_dict(unique_wilds(term[1]), size)


def unique_wilds(term):
    '''
    List of all different occurring 'Xs'.
    '''
    return sorted(list(set(wilds(term))))


def wilds(term):
    '''
    List of all occurring 'Xs'.
    '''
    return sorted(findall(r'X\d+', term))


def init_dict(keys, length):
    d = {}
    for k in keys:
        d[k] = ['']*length
    return d


def configs_to_table(configs, size):
    '''

    :param configs: [{'X1':'A', 'X3':'(A->B)'},{'X1':'C', 'X3':'C'},{...}], second return argument of cs, compare_to
    :param size: highest Xn that occurs for one atomic Formula.
    :return: table:
    Example:
              X1  X2  X3  X4
        [   [   ,   ,   ,   ],
            [   ,   ,   ,   ],
            ...
            [   ,   ,   ,   ]
        ]
    '''
    # init empty matrix of needed size
    # e.g.: x_size = 5, len(cs) = 3
    # >> configs = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]
    table = [['' for i in range(size)] for j in range(len(configs))]

    row = 0
    for line in configs:
        for x in line:
            position = int(x[1:]) - 1
            term = line[x]
            table[row][position] = term
        row += 1
    return table


def merge_two_tables(first, second):
    '''

    :param first:
    :param second:
    :return:
    '''
    # init empty match
    match = [['']*len(first[0])]
    # holds all matches
    merged_tables = []
    for condition in first:
        for candidate in second:
            m = merge(condition, candidate)
            if m:
                merged_tables.append(m)
    return merged_tables

