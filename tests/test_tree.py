import unittest
from tree import Tree


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
        tree = Tree('(a:F)')
        self.assertEqual('(a:F)', tree.to_s())
        tree = Tree('((!a):F)')
        self.assertEqual('((!a):F)', tree.to_s())
        tree = Tree('((a*(!(b+c))):F)')
        self.assertEqual('((a*(!(b+c))):F)', tree.to_s())
        tree = Tree('(((f+e)*d)+((!b)+a))')
        self.assertEqual('(((f+e)*d)+((!b)+a))', tree.to_s())
        tree = Tree('((a*(!b))*(!c))')
        self.assertEqual('((a*(!b))*(!c))', tree.to_s())
        t = Tree('((a*(!b)):F)')
        self.assertEqual('((a*(!b)):F)', t.to_s())
        monster = Tree('(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)')
        self.assertEqual('(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)', monster.to_s())
        yig = Tree('(((!(a*b))+(c*((!d)+e))):((a*b):F))')
        self.assertEqual('(((!(a*b))+(c*((!d)+e))):((a*b):F))', yig.to_s())
        tree = Tree('((((a*(!b))+a)*(b*a)):F)')
        self.assertEqual('((((a*(!b))+a)*(b*a)):F)', tree.to_s())
        tree = Tree('((((((!A)*B)+(C+D))*((!E)+(F+G)))*(H*I)):F)')
        self.assertEqual('((((((!A)*B)+(C+D))*((!E)+(F+G)))*(H*I)):F)', tree.to_s())

    def test_subtree(self):
        tree = Tree('((a*(!(b+c))):F)')
        node = tree.root.left
        subtree = tree.subtree(node)
        self.assertEqual('*', subtree.root.token)
        self.assertEqual('(a*(!(b+c)))', subtree.to_s())

    def test_inorder_nodes(self):
        tree = Tree('((a*(!(b+c))):F)')
        nodes = []
        for node in tree.preorder_nodes(tree.root):
            nodes.append(node.token)
        self.assertListEqual([':', '*', 'a', '!', '+', 'b', 'c', 'F'], nodes)

    def test_first1(self):
        tree = Tree('((a*(!(b+c))):F)')
        mult = tree.root.left
        bang = tree.root.left.right
        plus = tree.root.left.right.right
        self.assertEqual(mult, tree.first('*'))
        self.assertEqual(bang, tree.first('!'))
        self.assertEqual(plus, tree.first('+'))

    def test_first2(self):
        tree = Tree('(a:((b+c)+d))')
        first_plus = tree.root.right
        self.assertEqual(first_plus, tree.first('+'))

    def test_has_bad_bang(self):
        f = Tree('((!a)*b)')
        self.assertTrue(f.has_bad_bang())
        f = Tree('(((!a)*b)*(!c))')
        self.assertTrue(f.has_bad_bang())
        f = Tree('((a*(!b))*(!c))')
        self.assertFalse(f.has_bad_bang())

    def test_leaves(self):
        tree = Tree('((a*(!b))*(!c))')
        a = []
        for leaf in tree.leaves(tree.root):
            a.append(leaf.token)
        self.assertListEqual(['a', 'b', 'c'], a)

    def test_proof_terms1(self):
        t = Tree('((a*b):F)')
        c = t.musts()
        self.assertListEqual([('a', '(X1->F)'), ('b', 'X1')], c)
        t = Tree('(((a*b)*c):F)')
        c = t.musts()
        self.assertListEqual([('a', '(X2->(X1->F))'), ('b', 'X2'), ('c', 'X1')], c)

    def test_proof_terms2(self):
        t = Tree('((a*(!b)):F)')
        c = t.musts()
        self.assertListEqual([('a', '((b:X2)->F)'), ('b', 'X2')], c)

    def test_proof_terms3(self):
        t = Tree('(((a*(b*c))*(!(d*(!e)))):F)')
        c = t.musts()
        self.assertListEqual([('a', '(X5->(((d*(!e)):X2)->F))'), ('b', '(X6->X5)'), ('c', 'X6'), ('d', '((e:X4)->X2)'), ('e', 'X4')], c)

    def test_left_split(self):
        t = Tree('(e*(f+g))')
        n = t.first('+')
        t.left_split(n)
        self.assertEqual('(e*f)', t.to_s())

    def test_right_split(self):
        t = Tree('(e*(f+g))')
        n = t.first('+')
        t.right_split(n)
        self.assertEqual('(e*g)', t.to_s())

    # def test_possible_match(self):
    #     a = Tree('(X3->((c:X2)->(c:F)))')
    #     self.assertEqual('(X3->((c:X2)->(c:F)))', a.to_s())
    #     b = Tree('(A->((c:A)->(c:F)))')
    #     self.assertEqual('(A->((c:A)->(c:F)))', b.to_s())
    #     match = Tree._possible_match(a.root, b.root)
    #     self.assertListEqual([('X3', 'A'), ('X2', 'A')], match)
    #
    # def test_possible_match2(self):
    #     a = Tree('(X3->((c:X2)->(c:F)))')
    #     b = Tree('(A->((c:B)->(c:F)))')
    #     match = Tree._possible_match(a.root, b.root)
    #     self.assertListEqual([('X3', 'A'), ('X2', 'B')], match)
    #
    # def test_possible_match3(self):
    #     a = Tree('(A->((c:B)->(c:F)))')
    #     b = Tree('(A->((c:Z)->(c:F)))')
    #     match = Tree._possible_match(a.root, b.root)
    #     self.assertFalse(match)
    #
    # def test_possible_match4(self):
    #     a = Tree('(A->((c:B)->(c:F)))')
    #     b = Tree('(A->((c:B)->(c:F)))')
    #     match = Tree._possible_match(a.root, b.root)
    #     self.assertListEqual([], match)
    #
    # def test_possible_match5(self):
    #     a = Tree('(X3->((c:X2)->(c:F)))')
    #     b = Tree('(((a*b):Z)->((c:Y)->(c:F)))')
    #     match = Tree._possible_match(a.root, b.root)
    #     self.assertListEqual([('X3', '((a*b):Z)'), ('X2', 'Y')], match)

    # def test_possible_match6(self):
    #     print('===')
    #     a = Tree('(X3->((c:X2)->(c:F)))')
    #     b = Tree('(A->((c:B)->(G)))')
    #     match = Tree._possible_match(a.root, b.root)
    #     self.assertFalse(match)
    #     print('===')
    #
    # def test_possible_match7(self):
    #     match = Tree.possible_match('(X2->(X1->F))', '(G->H)')
    #     self.assertFalse(match)
    #
    # def test_possible_match8(self):
    #     a = Tree('(B->F)')
    #     b = Tree('(A->T)')
    #     match = Tree._possible_match(a.root, b.root)
    #     self.assertFalse(match)
    #
    # def test_possible_match9(self):
    #     a = Tree('(X1->T)')
    #     b = Tree('(A->B)')
    #     match = Tree._possible_match(a.root, b.root)
    #     self.assertFalse(match)
    #
    # # def test_possible_match9(self):
    # #     a = Tree('(X1->F)')
    # #     b = Tree('(A->T)')
    # #     match = Tree._possible_match(a.root, b.root)
    # #     self.assertFalse(match)
    #

    def test_mismatch_search1(self):
        a = Tree('(A->B)')
        b = Tree('(A->C)')
        x = Tree('(X1->B)')
        mismatch, wilds = Tree._mismatch_search(a.root, a.root)
        self.assertListEqual([], mismatch)
        self.assertListEqual([], wilds)
        mismatch, wilds = Tree._mismatch_search(a.root, b.root)
        self.assertTrue(mismatch[0])
        self.assertListEqual([], wilds)
        mismatch, wilds = Tree._mismatch_search(x.root, a.root)
        self.assertListEqual([], mismatch)
        self.assertListEqual([('X1', 'A')], wilds)
        mismatch, wilds = Tree._mismatch_search(x.root, b.root)
        self.assertTrue(mismatch[0])
        self.assertListEqual([('X1', 'A')], wilds)
