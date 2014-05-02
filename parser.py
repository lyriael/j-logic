#testdata
cs = {'a': 'A', 'b': 'B', 'c': 'C'}
formulas = ['(a+b):B', '(a+b):A', 'b!:(b:B)', '(b!+c):(b:B)', '((a+b)+c):C']


def clean_braces(expression):
    #todo: what about (a+b)+(c+d) ??, also the bintree needs braces around two-op-term, but none about single-op-term
    if expression[:1] == '(' and expression[-1:] == ')':
        return expression[1:-1]
    return expression


def within_braces(expression, position):
    '''
    Checks if the character of the given position is wrapped within braces.
    '''
    left_found = False
    right_found = False

    #go right
    for c in expression[position+1:]:
        if c == '(':
            break
        if c == ')':
            right_found = True
            break
    #go left
    for c in expression[position-1::-1]:
        if c == ')':
            break
        if c == '(':
            left_found = True
            break
    return left_found and right_found


def not_within_braces(expression, position):
    return not within_braces(expression, position)


def find_right_most_colon(expression):
    for i, c in enumerate(expression[::-1]):
        if c == ':':
            position = len(expression) - (i+1)
            print("Found one at position {}:".format(position))
            if not_within_braces(expression, position):
                print("Return {}.".format(position))
                return position
            else:
                print("Is within braces.")
    return

#print("Is not within braces: {}".format(not_within_braces(formulas[3], 6)))
#print(find_right_most_colon(formulas[3]))