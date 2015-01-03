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


def x_size(musts):
    '''
    Takes an list of tuples as input and
    searches for to highest occurring X..
    '''
    all_xs = []
    for term in musts:
        all_xs += wild_list(term[1])
    all_xs = sorted(list(set(all_xs)))
    #todo: fix this!
    if len(all_xs) == 0:
        return 0
    return sorted(map(lambda x: int(x[1:]), all_xs)).pop()


def simple_merge(a, b):
    '''
    compares to lists, if they are mergeable return the merge, else return None.
    '''
    size = len(a)
    new = ['']*size
    for index in range(size):
        # first check if wilds match
        if a[index] == b[index]:
            new[index] = a[index]

        elif a[index] == '':
            new[index] = b[index]

        elif b[index] == '':
            new[index] = a[index]
        else:
            return None
    return new


def update_condition_with_x(term, list):
    for i in range(len(list)):
        if list[i] != '':
            x = 'X'+str(i+1)
            term = term.replace(x, list[i])
    return term


def has_no_wilds(term):
    return not ('X' in term or 'Y' in term)


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


def unique_wilds(term):
    '''
    List of all different occurring 'Xs'.
    '''
    return sorted(list(set(wild_list(term))))


def wild_list(term):
    '''
    List of all occurring 'Xs'.
    '''
    return sorted(findall(r'X\d+', term))


def configs_to_table(configs, size):
    '''

    :param configs: [   ({'X1':'A', 'X3':'(A->B)'}, [('X2', 'X1')]  ),
                        ({'X1':'C', 'X3':'C'},      []              ),
                        ({...},                     []              )],
                        second return argument of cs, compare_to
    :param size: highest Xn that occurs for one atomic Formula.
    :return: table:
    Example:
              X1  X2  X3  X4    conditions
        [   ([   ,   ,   ,   ],  None)
            ([   ,   ,   ,   ],  [...])
            ...
            ([   ,   ,   ,   ],  None)
        ]
    '''
    # init empty matrix of needed size
    # e.g.: x_size = 5, len(cs) = 3
    # >> table = [(['', '', '', '', ''], []), (['', '', '', '', ''], []), (['', '', '', '', ''], [])]
    if configs:
        table = [['' for i in range(size)] for j in range(len(configs))]
        finale_table = []
        row = 0
        for tpl in configs:
            for x in tpl[0]: # accessing the wild-dict, ignoring conditions (tpl[1])
                position = int(x[1:]) - 1
                term = tpl[0][x]
                table[row][position] = term
            t = (table[row], tpl[1])
            finale_table.append(t)
            row += 1
        return finale_table
    else:
        return [(['']*size, [])]


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


def rename_dict_from_x_to_y_wilds(wilds):
    y_wilds = {}
    for key in wilds:
        y_key = str('Y'+key[1:])
        y_wilds[y_key] = wilds[key]
    return y_wilds


def uniq(some_list):
    uniq_list = []
    for item in some_list:
        if item not in uniq_list:
            uniq_list.append(item)
    return uniq_list