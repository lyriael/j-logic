import unittest
from formula import Formula
from tree_node import Node


class Tests(unittest.TestCase):

    def test_make_tree1(self):
        tree = Node.make_tree('(!(a+b))')
        self.assertEqual('(!(a+b))', str(tree))
        self.assertEqual('!', tree.token())

    def test_make_tree2(self):
        tree = Node.make_tree('((!a)+b)')
        self.assertTrue(tree.is_root())
        self.assertEqual('+', tree.root().token())
        self.assertEqual(tree, tree.root())
        self.assertEqual('!', tree.left().token())
        self.assertIsNone(tree.left().left())
        self.assertEqual('a', tree.left().right().token())
        self.assertIsNone(tree.left().right().left())
        self.assertIsNone(tree.left().right().right())
        self.assertEqual('b', tree.right().token())
        self.assertTrue(tree.right().is_leaf())

    def test_is_left_son_of1(self):
        node = Node.make_tree('((!a)+b)')
        left = node.left()
        self.assertEqual('!', left.token())
        self.assertTrue(left.is_left_son_of('+'))

    def test_is_left_son_of2(self):
        node = Node.make_tree('(b*(!a))')
        self.assertEqual('!', node.right().token())
        self.assertFalse(node.right().is_left_son_of('*'))

    ## function depricated
    # def test_remove_invalid_subtree1(self):
    #     tree = Node.make_tree('((!a)*b)')
    #     self.assertEqual(4, len(tree))
    #     tree.remove_invalid_subtree()
    #     self.assertEqual(2, len(tree))
    #     self.assertEqual('*', tree.token())
    #     self.assertIsNone(tree.left())
    #     self.assertEqual('b', tree.right().token())
    #     self.assertTrue(tree.is_root())
    #     self.assertTrue(tree.right().is_leaf())

    def test_tidy_up_ll(self):
        tree = Node.make_tree('(((!a)+A)*B)')
        self.assertEqual('*', tree.token())
        self.assertEqual('B', tree.right().token())
        self.assertTrue(tree.right().is_leaf())
        self.assertEqual('+', tree.left().token())
        self.assertEqual(6, len(tree))
        self.assertEqual('(((!a)+A)*B)', str(tree))
        bang = tree.left().left()
        self.assertEqual('!', bang.token())
        bang.tidy_up()
        self.assertEqual(3, len(tree))

    # def test_tidy_up_rl(self):
    #     tree = Node.make_tree('(B*(A+(!a)))')
    #     self.assertEqual('(B*(A+(!a)))', str(tree))
    #     self.assertEqual(6, len(tree))
    #     bang = tree.right().left()
    #     self.assertEqual('!', bang.token())
    #     bang.tidy_up()
    #     self.assertEqual(3, len(tree))

    def test_tidy_up_rr(self):
        tree = Node.make_tree('(B*(A+(!a)))')
        self.assertEqual('(B*(A+(!a)))', str(tree))
        self.assertEqual(6, len(tree))
        bang = tree.right().right()
        self.assertEqual('!', bang.token())
        bang.tidy_up()
        self.assertEqual(3, len(tree))

    def test_tidy_up_lr(self):
        tree = Node.make_tree('((A+(!a))*B)')
        self.assertEqual('((A+(!a))*B)', str(tree))
        self.assertEqual(6, len(tree))
        bang = tree.left().right()
        self.assertEqual('!', bang.token())
        bang.tidy_up()
        self.assertEqual(3, len(tree))

    # def test_tidy_up5(self):
    #     tree = Node.make_tree('((A*(!a))*B)')
    #     bang = tree.left().right()
    #     print(tree)
    #     bang.tidy_up()
    #     print(tree)
    #     self.assertEqual(1, len(tree))

    #todo: test tidy_up where + is not next operation

    # def test_is_in_subtree1(self):
    #     node = Node.make_tree('((!a)+b)')
    #     left = node.left()
    #     self.assertEqual('!', left.token())
    #     self.assertTrue(node.in_subtree('!'))
    #     self.assertTrue(node.in_subtree('!', 'left'))
    #     self.assertFalse(node.in_subtree('!', 'right'))

    def test_is_in_subtree2(self):
        node = Node.make_tree('((A+(!a))*B)')
        self.assertEqual('((A+(!a))*B)', str(node))
        self.assertEqual(6, len(node))
        self.assertEqual('!', node.left().right().token())
        self.assertTrue(node.in_subtree('!', 'left'))
        # print('====')
        # self.assertTrue(node.in_subtree('!'))
        # self.assertFalse(node.in_subtree('!', 'right'))
