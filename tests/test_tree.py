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

    def test__replace_in_tree(self):
        y = Tree('(Y1->(Y2->Y1))')
        x = Tree('X1')
        Tree._replace_in_tree(y.root, 'Y1', x.root)
        self.assertEqual('(X1->(Y2->X1))', y.to_s())

    def test_compare_second_try1(self):
        a = Tree('((A->B)->C)')
        x = Tree('(X1->X2)')
        con, wil = Tree.compare_second_try(x.root, a.root, [], {})
        self.assertListEqual(con, [])
        self.assertDictEqual(wil, {'X2': 'C', 'X1': '(A->B)'})

    def test_compare_second_try2(self):
        a = Tree('((A->B)->C)')
        y = Tree('(Y1->Y2)')
        con, wil = Tree.compare_second_try(a.root, y.root, [], {})
        self.assertListEqual(con, [])
        self.assertDictEqual(wil, {})

    def test_compare_second_try3(self):
        cs = Tree('(Y1->Y2)')
        orig = Tree('((X1->X2)->X3)')
        con, wil = Tree.compare_second_try(orig.root, cs.root, [], {})
        self.assertListEqual(con, [])
        self.assertDictEqual(wil, {})

    def test_compare_second_try4(self):
        cs = Tree('(A->B)')
        orig = Tree('(X1->(X2->X3))')
        con, wil = Tree.compare_second_try(orig.root, cs.root, [], {})
        self.assertIsNone(con)
        self.assertIsNone(wil)

    def test_compare_second_try5(self):
        cs = Tree('(Y1->(Y2->Y1))')
        orig = Tree('(X3->(X2->(X1->F)))')
        con, wil = Tree.compare_second_try(orig.root, cs.root, [], {})
        self.assertListEqual(con, [('X3', '(X1->F)')])
        self.assertDictEqual(wil, {})

    def test_compare_second_try6(self):
        cs = Tree('(Y1->(Y1->Y1))')
        orig = Tree('(X3->(X2->(X1->F)))')
        con, wil = Tree.compare_second_try(orig.root, cs.root, [], {})
        self.assertListEqual(con, [('X3', 'X2'), ('X3', '(X1->F)')])
        self.assertDictEqual(wil, {})

    def test_compare_second_try7(self):
        cs = Tree('(Y1->Y1)')
        orig = Tree('((A->B)->A)')
        con, wil = Tree.compare_second_try(orig.root, cs.root, [], {})
        self.assertIsNone(con)
        self.assertIsNone(wil)

    def test_compare_second_try8(self):
        cs = Tree('(Y1->(Y2->Y1))')
        orig = Tree('((X1->F)->(B->(X2->G)))')
        con, wil = Tree.compare_second_try(orig.root, cs.root, [], {})
        self.assertIsNone(con)
        self.assertIsNone(wil)

    def test_compare_second_try9(self):
        cs = Tree('(Y1->(Y1->Y1))')
        orig = Tree('(X1->(B->X2))')
        con, wil = Tree.compare_second_try(orig.root, cs.root, [], {})
        self.assertListEqual(con, [('X1', 'X2')])
        self.assertDictEqual(wil, {'X1': 'B'})

    def test_compare_second_try10(self):
        cs = Tree('(Y1->(Y1->F))')
        orig = Tree('(X1->X2)')
        con, wil = Tree.compare_second_try(orig.root, cs.root, [], {})
        self.assertListEqual(con, [('X2', '(X1->F)')])
        self.assertDictEqual(wil, {})

    def test_compare_second_try11(self):
        cs = Tree('(Y1->(Y2->F))')
        orig = Tree('(X1->X2)')
        con, wil = Tree.compare_second_try(orig.root, cs.root, [], {})
        self.assertListEqual(con, [('X2', '(Y2->F)')])
        self.assertDictEqual(wil, {})

    def test_compare_second_try12(self):
        cs = Tree('((Y1->(Y2->F))->(Y1->G))')
        orig = Tree('((X1->X2)->X3)')
        con, wil = Tree.compare_second_try(orig.root, cs.root, [], {})
        self.assertListEqual(con, [('X2', '(Y2->F)'), ('X3', '(X1->G)')])
        self.assertDictEqual(wil, {})

    def test_compare_second_try13(self):
        cs = Tree('((Y1->(Y2->F))->(Y2->G))')
        orig = Tree('((X1->X2)->X3)')
        con, wil = Tree.compare_second_try(orig.root, cs.root, [], {})
        self.assertListEqual(con, [('X2', '(Y2->F)'), ('X3', '(Y2->G)')])
        self.assertDictEqual(wil, {})

    def test_compare_second_try14(self):
        cs = Tree('((Y1->Y2)->(Y1->Y1))')
        orig = Tree('(X3->(X2->(X1->F)))')
        con, wil = Tree.compare_second_try(orig.root, cs.root, [], {})
        self.assertListEqual(con, [('X3', '(Y1->Y2)'), ('X2', '(X1->F)')])
        self.assertDictEqual(wil, {})

    def test_sum_split1(self):
        f = Tree('((a+b):F)')
        self.assertEqual(2, len(f._sum_split()))
        # print(f.sum_split()[0].tree.to_s())
        # print(f.sum_split()[1].tree.to_s())

    def test_sum_split2(self):
        f = Tree('((((f+e)*d)+((!b)+a)):F)')
        self.assertEqual(4, len(f._sum_split()))
        # for g in f.sum_split():
        #     print(g.formula)

    def test_sum_split3(self):
        f = Tree('(((a*b)+(a*b)):F)')
        self.assertEqual(1, len(f._sum_split()))

    def test_sum_split4(self):
        f = Tree('((e*(f+g)):F)')
        self.assertEqual(2, len(f._sum_split()))
        s = []
        for term in f._sum_split():
            s.append(term.to_s())
        self.assertListEqual(['((e*f):F)', '((e*g):F)'], sorted(s))

    def test_sum_split5(self):
        monster = Tree('(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)')
        many_formulas = monster._sum_split()
        a = []
        for f in many_formulas:
            a.append(f.to_s())
        self.assertListEqual(['((!((!a)*(c*(!d)))):F)', '((!(b*(c*(!d)))):F)',
                              '((e*f):F)', '((e*g):F)'], sorted(a))

    def test_remove_bang1(self):
        f = Tree('((!a):(a:A)))')
        self.assertEqual('(a:A)', f._simplify_bang().to_s())
        f = Tree('((!((a+b)*c)):(((a+b)*c):F))')
        self.assertEqual('(((a+b)*c):F)', f._simplify_bang().to_s())

    def test_remove_bang2(self):
        f = Tree('((!((a+b)*c)):((b*c):F))')
        self.assertIsNone(f._simplify_bang())