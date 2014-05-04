from formula import Formula


cs = {'a': 'A', 'b': 'B', 'c': 'C'}
f1 = '((a+!b):A)'
f2 = '(a:A)'
f3 = '((a+!b):(b:B))'


def run_all():
    print('RUN ALL:')
    print('-----------')
    test_init()
    # test_is_provable_1()
    # test_is_provable_2()
    test_is_provable_3()


def test_init():
    print('test_init')
    formula = Formula(f2)
    assert str(formula) == '(a:A)'
    formula = Formula(f1)
    assert str(formula) == f1
    formula2 = Formula(formula._tree.left())
    assert str(formula2) == '(a+!b)'
    print('ok---------')


def test_is_provable_1():
    print('is_provable_1')
    formula = Formula(f1)
    assert formula.is_provable(cs)


def test_is_provable_2():
    print('is_provable_2')
    formula = Formula(f2)
    assert formula.is_provable(cs)


def test_is_provable_3():
    print('is_provable_3')
    formula = Formula(f3)
    assert formula.is_provable(cs)


run_all()
