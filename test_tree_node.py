from tree_node import Node


def test_simple_addition():
    print('test tree for: (a+b)')
    test1 = '(a+b)'
    tree1 = Node.make_tree(test1)
    assert tree1.inorder() == '(a+b)'
    assert len(tree1) == 3
    print('-----------ok------------')


def test_with_proof_term_1():
    print('test tree for: (a:A)')
    term = '(a:A)'
    tree = Node.make_tree(term)
    #print('root: ' + tree.token + ', left: ' + tree.get_left().token + ', right: ' + tree.get_right().token)
    assert tree.inorder() == '(a:A)'
    assert len(tree) == 3
    print('-----------ok------------')


def test_with_proof_term_2():
    print('test tree for: ((c+(a+b)):A)')
    term = '((c+(a+b)):A)'
    tree = Node.make_tree(term)
    #print(tree.token)
    assert tree.inorder() == '((c+(a+b)):A)'
    assert len(tree) == 7
    print('-----------ok------------')


def test_with_bang_1():
    print('test tree for: (!a+b)')
    tree = Node.make_tree('(!a+b)')
    assert tree.inorder() == '(!a+b)'
    assert len(tree) == 4
    print('-----------ok------------')



def run_all():
    test_simple_addition()
    test_with_proof_term_1()
    test_with_proof_term_2()
    test_with_bang_1()


run_all()


