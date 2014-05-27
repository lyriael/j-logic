import unittest
from formula import Formula
from tree_node import Node

class Tests(unittest.TestCase):

    def test_make_tree1(self):
        tree = Node.make_tree('(!(a+b))')
        self.assertEqual('(!(a+b))', str(tree))
        self.assertEqual('!', tree.token())

    def test_is_left_son_of1(self):
        node = Node.make_tree('((!a)+b)')
        left = node.left()
        self.assertEqual('!', left.token())
        self.assertTrue(left.is_left_son_of('+'))
