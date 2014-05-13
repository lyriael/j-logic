from formula import Formula


cs = {'a': 'A', 'b': 'B', 'c': 'C'}
f1 = '((a+!b):A)'
f2 = '(a:A)'
f3 = '((a+!b):(b:B))'
f4 = '((!a+b):(b:B))'

tests = [0, 1, 2, 3, 4]


def run_all(those):
    print('--------------------------')
    print('| RUN ALL TESTS:         |')
    print('--------------------------')
    print('')
    if 0 in those:
        test_init()
        print('=========================================================\n')
    if 1 in those:
        test_is_provable_1()
        print('=========================================================\n')
    if 2 in those:
        test_is_provable_2()
        print('=========================================================\n')
    if 3 in those:
        test_is_provable_3()
        print('=========================================================\n')
    if 4 in those:
        test_is_not_provable_4()
        print('=========================================================\n')


def test_init():
    print("------test init-----------\n")
    formula = Formula(f2)
    assert str(formula) == '(a:A)'
    formula = Formula(f1)
    assert str(formula) == f1
    formula2 = Formula(formula._tree.left())
    assert str(formula2) == '(a+!b)'
    print(' ok\n')


def test_is_provable_1():
    print("-----is provable f1--------\n")
    formula = Formula(f1)
    assert formula.is_provable(cs)


def test_is_provable_2():
    print("-----is provable f2--------\n")
    formula = Formula(f2)
    assert formula.is_provable(cs)


def test_is_provable_3():
    print("-----is provable f3--------\n")
    formula = Formula(f3)
    assert formula.is_provable(cs)

def test_is_not_provable_4():
    print("-----is not provable f4--------\n")
    formula = Formula(f4)
    assert not formula.is_provable(cs)


run_all(tests)
