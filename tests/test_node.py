import unittest
from node import Node


class Tests(unittest.TestCase):

    def test_init(self):
        node = Node()
        self.assertEqual('', node.token)
        self.assertEqual('', node.token)
        self.assertIsNone(node.parent)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
        self.assertIsNone(node.sibling)
        self.assertTrue(node.is_lonely())
        self.assertFalse(node.is_root())

    def init_sibling(self):
        right = Node()
        left = Node()
        right.sibling = left
        left.sibling = right
        self.assertEqual(right, left.sibling)
        self.assertEqual(left, right.sibling)

    def test_set_root(self):
        node = Node()
        node.set_root()
        self.assertTrue(node.is_root())
        self.assertEqual('root', node.position)
        self.assertFalse(node.is_lonely())
        self.assertTrue(node.is_leaf())

    def test_new_right(self):
        root = Node()
        root.set_root()
        right = root.new_right()
        self.assertTrue(root.has_right())
        self.assertFalse(root.has_left())
        self.assertEqual(root.right, right)
        self.assertEqual(right.parent, root)
        self.assertFalse(root.is_leaf())
        self.assertFalse(right.is_root())
        self.assertTrue(right.is_leaf())
        self.assertEqual('right', right.position)

    def test_new_left(self):
        root = Node()
        root.set_root()
        left = root.new_left()
        self.assertTrue(root.has_left())
        self.assertFalse(root.has_right())
        self.assertEqual(root.left, left)
        self.assertEqual(left.parent, root)
        self.assertFalse(root.is_leaf())
        self.assertFalse(left.is_root())
        self.assertTrue(left.is_leaf())
        self.assertEqual('left', left.position)

    def test_new_right_and_left(self):
        root = Node()
        root.set_root()
        right = root.new_right()
        left = root.new_left()
        self.assertEqual(right.sibling, left)
        self.assertEqual(left.sibling, right)

    def test_parse_tree_manual(self):
        # term: ((!a):F)
        root = Node()
        current = root
        current.set_root()
        self.assertEqual(root, current)
        # '('
        current = root.new_left()
        bang = current
        # '('
        current = bang.new_left()
        waste = current
        # '!'
        current = current.parent
        self.assertEqual(bang, current)
        current.token = '!'
        self.assertEqual('!', bang.token)
        current.left = None
        self.assertIsNone(bang.left)
        current = current.new_right()
        a = current
        # 'a'
        current.token = 'a'
        self.assertEqual('a', a.token)
        current = current.parent
        self.assertEqual(bang, current)
        # ')'
        current = current.parent
        self.assertEqual(current, root)
        # ':'
        current.token = ':'
        self.assertEqual(':', root.token)
        current = current.new_right()
        F = current
        # 'F'
        current.token = 'F'
        self.assertEqual('F', F.token)
        current = current.parent
        self.assertEqual(root, current)
        # ')'
        current = current.parent
        self.assertEqual(root, current)

