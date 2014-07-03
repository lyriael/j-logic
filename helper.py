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


def replace(consts, swaps):
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
    return sorted(list(set(wilds(term))))


def wilds(term):
    return sorted(findall(r'X\d+', term))


def init_dict(keys, length):
    d = {}
    for k in keys:
        d[k] = ['']*length
    return d