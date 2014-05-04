from tree_node import Node


def run_all():
    print('-----RUN ALL TESTS-------')
    test_init_one()
    test_properties_has_and_is_one()
    test_get_root()
    test_parent_relation()
    test_tree_properties()
    test_tree_getter_and_setter()
    test_inorder()
    test_subtree()
    test_simple_addition()
    test_with_proof_term_1()
    test_with_proof_term_2()
    test_with_bang_1()
    test_with_bang_2()
    test_print_subtree()


def test_init_one():
    node = Node()
    assert node._right is None
    assert node._left is None
    assert node._parent is node
    assert node._token == 'no token'
    print('--test_init_one--')


def test_properties_has_and_is_one():
    node = Node()
    assert node.is_root
    assert node.is_leaf()
    assert not node.has_left()
    assert not node.has_right()
    assert not node.is_tree()
    assert node.parent() == node
    assert node.token() == node.value() == 'no token'
    assert len(node) == 1
    print('--test_properties_has_and_is_one--')


def test_get_root():
    g1 = Node()
    g2 = Node()
    g3 = Node()
    g1._left = g2
    g2._parent = g1
    g2._left = g3
    g3._parent = g2
    assert g1.root() == g1
    assert g2.root() == g1
    assert g3.root() == g1
    print('--test_get_root--')


def test_parent_relation():
    parent = Node()
    child = Node()
    assert not child.is_tree()
    assert not parent.is_tree()
    child._parent = parent
    parent._left = child
    assert child.is_tree()
    assert parent.is_tree()
    assert child.parent() == parent
    print('--test_parent_relation--')


def test_tree_properties():
    root = Node()
    left = Node()
    right = Node()
    root._left = left
    root._right = right
    left._parent = root
    right._parent = root
    assert left.is_leaf()
    assert not left.is_root()
    assert right.is_leaf()
    assert not right.is_root()
    assert root.is_root()
    assert not root.is_leaf()
    assert left.parent() == right.parent() == root
    assert root.token() == left.token() == right.token() == 'no token'
    assert len(right) == len(left) == 1
    assert len(root) == 3
    print('--test_tree_properties--')


def test_tree_getter_and_setter():
    root = Node()
    left = root.new_left()
    right = root.new_right()
    assert left is not None
    assert right is not None
    assert root.is_root()
    assert not root.is_leaf()
    assert left.is_leaf()
    assert right.is_leaf()
    assert not left.is_root()
    assert not right.is_root()
    assert left.root() == right.root() == root
    assert root.left() == left
    assert root.right() == right
    assert root == left.parent() == right.parent()
    print('--test_tree_getter_and_setter--')


def test_inorder():
    s1 = '(a+b)'
    s2 = '((a+!b):A)'
    root = Node.make_tree(s1)
    assert root.inorder() == '(a+b)'
    assert root.left().inorder() == 'a'
    assert root.right().inorder() == 'b'
    # more complicated string:
    root = Node.make_tree(s2)
    assert root.inorder() == '((a+!b):A)'
    assert root.left().inorder() == '(a+!b)'
    assert root.right().inorder() == 'A'
    assert root.left().right().inorder() == '!b'
    print('--test_inorder--')


def test_subtree():
    tree = Node.make_tree('((a+!b):A)')
    node = tree.left()
    subtree = node.subtree()
    assert subtree.inorder() == tree.left().inorder() == '(a+!b)'
    print('--test_subtree--')


def test_simple_addition():
    print('--test_simple_addition--')
    print('--> test tree for: (a+b)')
    test = '(a+b)'
    tree = Node.make_tree(test)
    assert str(tree) == '(a+b)'
    assert len(tree) == 3


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


def test_with_bang_2():
    print('test tree for: ((a+!b):A)')
    tree = Node.make_tree('((a+!b):A)')
    assert tree.inorder() == '((a+!b):A)'
    assert len(tree) == 6
    print('-----------ok------------')


def test_print_subtree():
    print('test printing subtree: ((a+!b):A)')
    tree = Node.make_tree('((a+!b):A)')
    print(str(tree.left()))
    assert str(tree.left()) == '(a+!b)'






run_all()


