import unittest
from tree import *


class Tests(unittest.TestCase):

    def test_init1(self):
        tree = Tree('(a:F)')
        self.assertTrue(tree.root.is_root())
        self.assertEqual('root', tree.root.position)
        self.assertEqual('left', tree.root.left.position)
        self.assertEqual(':', tree.root.token)
        self.assertEqual('F', tree.root.right.token)
        self.assertEqual('a', tree.root.left.token)

    def test_init2(self):
        tree = Tree('((!a):F)')
        self.assertEqual(':', tree.root.token)
        self.assertEqual('!', tree.root.left.token)
        self.assertIsNone(tree.root.left.left)
        self.assertEqual('a', tree.root.left.right.token)
        self.assertTrue(tree.root.left.right.is_leaf())
        self.assertEqual('F', tree.root.right.token)
        self.assertTrue(tree.root.right.is_leaf())
        self.assertEqual(tree.root.left, tree.root.right.sibling)

    def test_init3(self):
        tree = Tree('((a*(!(b+c))):F)')
        self.assertEqual(':', tree.root.token)
        self.assertEqual('*', tree.root.left.token)
        self.assertEqual('a', tree.root.left.left.token)
        self.assertTrue(tree.root.left.left.is_leaf())
        self.assertIsNone(tree.root.left.right.left)
        self.assertEqual('!', tree.root.left.right.token)
        self.assertEqual('!', tree.root.left.left.sibling.token)
        self.assertEqual('b', tree.root.left.right.right.left.token)
        self.assertEqual('c', tree.root.left.right.right.right.token)

    def test_to_s(self):
        self.assertEqual('(a:F)', str(Tree('(a:F)')))
        self.assertEqual('((!a):F)', str(Tree('((!a):F)')))
        self.assertEqual('((a*(!(b+c))):F)', str(Tree('((a*(!(b+c))):F)')))
        self.assertEqual('(((f+e)*d)+((!b)+a))', str(Tree('(((f+e)*d)+((!b)+a))')))
        self.assertEqual('((a*(!b))*(!c))', str(Tree('((a*(!b))*(!c))')))
        self.assertEqual('((a*(!b)):F)', str(Tree('((a*(!b)):F)')))
        self.assertEqual('(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)',
                         str(Tree('(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)')))
        self.assertEqual('(((!(a*b))+(c*((!d)+e))):((a*b):F))', 
                         str(Tree('(((!(a*b))+(c*((!d)+e))):((a*b):F))')))
        self.assertEqual('((((a*(!b))+a)*(b*a)):F)', 
                         str(Tree('((((a*(!b))+a)*(b*a)):F)')))
        self.assertEqual('((((((!A)*B)+(C+D))*((!E)+(F+G)))*(H*I)):F)', 
                         str(Tree('((((((!A)*B)+(C+D))*((!E)+(F+G)))*(H*I)):F)')))
        self.assertEqual('(((((a*b)*((a*c)+(!c)))+(!(a+b)))+((a+(!b))*(b*a))):(a:F))',
                         str(Tree('(((((a*b)*((a*c)+(!c)))+(!(a+b)))+((a+(!b))*(b*a))):(a:F))')))
        self.assertEqual('(((!(a+c))+((a+(!a))*(b*(!c)))):(c:F))',
                         str(Tree('(((!(a+c))+((a+(!a))*(b*(!c)))):(c:F))')))

    def test_subtree(self):
        tree = Tree('((a*(!(b+c))):F)')
        node = tree.root.left
        st = subtree(node)
        self.assertEqual('*', st.root.token)
        self.assertEqual('(a*(!(b+c)))', str(st))

    def test_inorder_nodes(self):
        tree = Tree('((a*(!(b+c))):F)')
        nodes = []
        for node in tree._preorder_nodes(tree.root):
            nodes.append(node.token)
        self.assertListEqual([':', '*', 'a', '!', '+', 'b', 'c', 'F'], nodes)

    def test_first1(self):
        tree = Tree('((a*(!(b+c))):F)')
        mult = tree.root.left
        introspection = tree.root.left.right
        plus = tree.root.left.right.right
        self.assertEqual(mult, tree.first('*'))
        self.assertEqual(introspection, tree.first('!'))
        self.assertEqual(plus, tree.first('+'))

    def test_first2(self):
        tree = Tree('(a:((b+c)+d))')
        first_plus = tree.root.right
        self.assertEqual(first_plus, tree.first('+'))

    def test_left_split(self):
        t = Tree('(e*(f+g))')
        n = t.first('+')
        t._left_split(n)
        self.assertEqual('(e*f)', str(t))

    def test_right_split(self):
        t = Tree('(e*(f+g))')
        n = t.first('+')
        t._right_split(n)
        self.assertEqual('(e*g)', str(t))