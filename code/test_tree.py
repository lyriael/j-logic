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
        self.assertEqual('(a:F)', Tree('(a:F)').to_s())
        self.assertEqual('((!a):F)', Tree('((!a):F)').to_s())
        self.assertEqual('((a*(!(b+c))):F)', Tree('((a*(!(b+c))):F)').to_s())
        self.assertEqual('(((f+e)*d)+((!b)+a))', Tree('(((f+e)*d)+((!b)+a))').to_s())
        self.assertEqual('((a*(!b))*(!c))', Tree('((a*(!b))*(!c))').to_s())
        self.assertEqual('((a*(!b)):F)', Tree('((a*(!b)):F)').to_s())
        self.assertEqual('(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)', 
                         Tree('(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)').to_s())
        self.assertEqual('(((!(a*b))+(c*((!d)+e))):((a*b):F))', 
                         Tree('(((!(a*b))+(c*((!d)+e))):((a*b):F))').to_s())
        self.assertEqual('((((a*(!b))+a)*(b*a)):F)', 
                         Tree('((((a*(!b))+a)*(b*a)):F)').to_s())
        self.assertEqual('((((((!A)*B)+(C+D))*((!E)+(F+G)))*(H*I)):F)', 
                         Tree('((((((!A)*B)+(C+D))*((!E)+(F+G)))*(H*I)):F)').to_s())
        self.assertEqual('(((((a*b)*((a*c)+(!c)))+(!(a+b)))+((a+(!b))*(b*a))):(a:F))',
                         Tree('(((((a*b)*((a*c)+(!c)))+(!(a+b)))+((a+(!b))*(b*a))):(a:F))').to_s())
        self.assertEqual('(((!(a+c))+((a+(!a))*(b*(!c)))):(c:F))',
                         Tree('(((!(a+c))+((a+(!a))*(b*(!c)))):(c:F))').to_s())

    def test_subtree(self):
        tree = Tree('((a*(!(b+c))):F)')
        node = tree.root.left
        subtree = tree.subtree(node)
        self.assertEqual('*', subtree.root.token)
        self.assertEqual('(a*(!(b+c)))', subtree.to_s())

    def test_inorder_nodes(self):
        tree = Tree('((a*(!(b+c))):F)')
        nodes = []
        for node in tree._preorder_nodes(tree.root):
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
        self.assertTrue(Tree.has_bad_bang('(((!a)*b):F)'))
        self.assertTrue(Tree.has_bad_bang('((((!a)*b)*(!c)):F)'))
        self.assertFalse(Tree.has_bad_bang('(((a*(!b))*(!c)):F)'))

    def test_musts(self):
        self.assertListEqual([('a', '(X1->F)'), ('b', 'X1')], Tree.musts('((a*b):F)'))
        self.assertListEqual([('a', '(X2->(X1->F))'), ('b', 'X2'), ('c', 'X1')], Tree.musts('(((a*b)*c):F)'))
        self.assertListEqual([('a', '((b:X2)->F)'), ('b', 'X2')], Tree.musts('((a*(!b)):F)'))
        self.assertListEqual([('a', '(X5->(((d*(!e)):X2)->F))'), ('b', '(X6->X5)'),
                              ('c', 'X6'), ('d', '((e:X4)->X2)'), ('e', 'X4')],
                             Tree.musts('(((a*(b*c))*(!(d*(!e)))):F)'))

    def test_left_split(self):
        t = Tree('(e*(f+g))')
        n = t.first('+')
        t._left_split(n)
        self.assertEqual('(e*f)', t.to_s())

    def test_right_split(self):
        t = Tree('(e*(f+g))')
        n = t.first('+')
        t._right_split(n)
        self.assertEqual('(e*g)', t.to_s())

    def test_replace_in_tree(self):
        y = Tree('(Y1->(Y2->Y1))')
        Tree._replace_in_tree(y.root, 'Y1', Tree('X1').root)
        self.assertEqual('(X1->(Y2->X1))', y.to_s())

    def test_compare01(self):
        con, wil = Tree.compare(Tree('(X1->X2)').root, Tree('((A->B)->C)').root, [], {})
        self.assertListEqual(con, [])
        self.assertDictEqual(wil, {'X2': 'C', 'X1': '(A->B)'})

    def test_unify01(self):
        dct = unify('(X1->X2)', '((A->B)->C)')
        self.assertDictEqual({'X1': ['(A->B)'], 'X2': ['C']}, dct)

    def test_compare02(self):
        con, wil = Tree.compare(Tree('((A->B)->C)').root, Tree('(Y1->Y2)').root, [], {})
        self.assertListEqual(con, [])
        self.assertDictEqual(wil, {})

    def test_compare03(self):
        con, wil = Tree.compare(Tree('((X1->X2)->X3)').root, Tree('(Y1->Y2)').root, [], {})
        self.assertListEqual(con, [])
        self.assertDictEqual(wil, {})

    def test_compare04(self):
        con, wil = Tree.compare(Tree('(X1->(X2->X3))').root, Tree('(A->B)').root, [], {})
        self.assertIsNone(con)
        self.assertIsNone(wil)

    def test_compare05(self):
        con, wil = Tree.compare(Tree('(X3->(X2->(X1->F)))').root, Tree('(Y1->(Y2->Y1))').root, [], {})
        self.assertListEqual(con, [('X3', '(X1->F)')])
        self.assertDictEqual(wil, {})

    def test_compare06(self):
        con, wil = Tree.compare(Tree('(X3->(X2->(X1->F)))').root, Tree('(Y1->(Y1->Y1))').root, [], {})
        self.assertListEqual(con, [('X3', 'X2'), ('X3', '(X1->F)')])
        self.assertDictEqual(wil, {})

    def test_compare07(self):
        con, wil = Tree.compare(Tree('((A->B)->A)').root, Tree('(Y1->Y1)').root, [], {})
        self.assertIsNone(con)
        self.assertIsNone(wil)

    def test_compare08(self):
        con, wil = Tree.compare(Tree('((X1->F)->(B->(X2->G)))').root, Tree('(Y1->(Y2->Y1))').root, [], {})
        self.assertIsNone(con)
        self.assertIsNone(wil)

    def test_compare09(self):
        con, wil = Tree.compare(Tree('(X1->(B->X2))').root, Tree('(Y1->(Y1->Y1))').root, [], {})
        self.assertListEqual(con, [('X1', 'X2')])
        self.assertDictEqual(wil, {'X1': 'B'})

    def test_compare10(self):
        con, wil = Tree.compare(Tree('(X1->X2)').root, Tree('(Y1->(Y1->F))').root, [], {})
        self.assertListEqual(con, [('X2', '(X1->F)')])
        self.assertDictEqual(wil, {})

    def test_compare11(self):
        con, wil = Tree.compare(Tree('(X1->X2)').root, Tree('(Y1->(Y2->F))').root, [], {})
        self.assertListEqual(con, [('X2', '(Y2->F)')])
        self.assertDictEqual(wil, {})

    def test_compare12(self):
        con, wil = Tree.compare(Tree('((X1->X2)->X3)').root, Tree('((Y1->(Y2->F))->(Y1->G))').root, [], {})
        self.assertListEqual(con, [('X2', '(Y2->F)'), ('X3', '(X1->G)')])
        self.assertDictEqual(wil, {})

    def test_compare13(self):
        con, wil = Tree.compare(Tree('((X1->X2)->X3)').root, Tree('((Y1->(Y2->F))->(Y2->G))').root, [], {})
        self.assertListEqual(con, [('X2', '(Y2->F)'), ('X3', '(Y2->G)')])
        self.assertDictEqual(wil, {})

    def test_compare14(self):
        con, wil = Tree.compare(Tree('(X3->(X2->(X1->F)))').root, Tree('((Y1->Y2)->(Y1->Y1))').root, [], {})
        self.assertListEqual(con, [('X3', '(Y1->Y2)'), ('X2', '(X1->F)')])
        self.assertDictEqual(wil, {})

    def test_compare15(self):
        con, wil = Tree.compare(Tree('(X1->(c:F))').root, Tree('(Y1->(Y2->Y3))').root, [], {})
        self.assertIsNone(con)
        self.assertIsNone(wil)

    def test_compare_x_and_y_mix1(self):
        con, wil = Tree.compare(Tree('(X2->X1)').root, Tree('(Y1->(Y2->Y1)').root, [], {})
        self.assertListEqual([('X1', '(Y2->X2)')], con)
        self.assertDictEqual({}, wil)

    def test_compare_x_and_y_mix2(self):
        con, wil = Tree.compare(Tree('((X1->F)->(B->(X2->G)))').root, Tree('(Y1->(Y2->Y1)').root, [], {})
        self.assertIsNone(con)
        self.assertIsNone(wil)

    # def test_compare_x_and_y_mix3(self):
    #     con, wil = Tree.compare(Tree('(Y2->B)').root, Tree('(A->Y1)').root, [], {})
    #     self.assertIsNone(con)
    #     self.assertIsNone(wil)

    def test_sum_split1(self):
        self.assertEqual(2, len(Tree.sum_split('((a+b):F)')))

    def test_sum_split2(self):
        self.assertEqual(4, len(Tree.sum_split('((((f+e)*d)+((!b)+a)):F)')))

    def test_sum_split3(self):
        self.assertEqual(1, len(Tree.sum_split('(((a*b)+(a*b)):F)')))

    def test_sum_split4(self):
        self.assertEqual(2, len(Tree.sum_split('((e*(f+g)):F)')))
        s = []
        for term in Tree.sum_split('((e*(f+g)):F)'):
            s.append(term)
        self.assertListEqual(['((e*f):F)', '((e*g):F)'], sorted(s))

    def test_sum_split5(self):
        many_formulas = Tree.sum_split('(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)')
        a = []
        for f in many_formulas:
            a.append(f)
        self.assertListEqual(['((!((!a)*(c*(!d)))):F)', '((!(b*(c*(!d)))):F)',
                              '((e*f):F)', '((e*g):F)'], sorted(a))

    def test_simplify_bang(self):
        self.assertEqual('(a:A)', Tree.simplify_bang('((!a):(a:A)))'))
        self.assertEqual('(((a+b)*c):F)', Tree.simplify_bang('((!((a+b)*c)):(((a+b)*c):F))'))
        self.assertEqual('', Tree.simplify_bang('((!((a+b)*c)):((b*c):F))'))
        self.assertEqual('(a:A)', Tree.simplify_bang('(a:A)'))

    def test_unify1(self):
        cons = unify('(X3->((a:X2)->(X1->F)))', '(Y1->(Y2->Y1))')
        # self.assertDictEqual({'X1': [], 'X2': [], 'X3': ['Y1'], 'Y1': ['(X1->F)', 'X3'], 'Y2': ['(a:X2)']}, cons)
        self.assertDictEqual({'X3': ['Y1'], 'Y1': ['(X1->F)', 'X3'], 'Y2': ['(a:X2)']}, cons)

    def test_unify2(self):
        cons = unify('(Y1->Y2)', 'X1')
        #self.assertDictEqual({'X1': ['(Y1->Y2)'], 'Y2': [], 'Y1': []}, cons)
        self.assertDictEqual({'X1': ['(Y1->Y2)']}, cons)

    def test_get_all_wilds(self):
        l = [('X1', '(A->Y2)'), ('Y2', 'X12'), ('A', 'X3')]
        v = get_all_wilds(l)
        self.assertListEqual(['X1', 'X12', 'X3', 'Y2'], v)

    def test_condition_list_to_dict(self):
        l = [('X1', '(A->Y2)'), ('Y2', 'X12'), ('A', 'X3')]
        d = condition_list_to_dict(l)
        self.assertDictEqual({'X3': ['A'], 'X12': ['Y2'], 'X1': ['(A->Y2)'], 'Y2': ['X12']}, d)

    def test_condition_list_to_dict2(self):
        l = [('X1', '(A->B)'), ('X1', '(X3->Y1)'), ('X1', '(X2->B)'), ('X2', '(X1->(B->C))'), ('X3', 'X1'), ('X1', '(X2->F)')]
        d = condition_list_to_dict(l)
        self.assertDictEqual({'X2': ['(X1->(B->C))'], 'X3': ['X1'], 'X1': ['(X2->F)', 'X3', '(X2->B)', '(A->B)', '(X3->Y1)']}, d)

    def test_condition_list_to_dict3(self):
        l = [('X1', '(X2->A)')]
        d = condition_list_to_dict(l)
        #self.assertDictEqual({'X2': [], 'X1': ['(X2->A)']}, d)
        self.assertDictEqual({'X1': ['(X2->A)']}, d)

    def test_condition_dict_to_list1(self):
        d = {'X1': [], 'X3': ['(X1->F)']}
        l = condition_dict_to_list(d)
        self.assertListEqual([('X3', '(X1->F)')], l)

    def test_condition_dict_to_list2(self):
        d = {'X1': []}
        l = condition_dict_to_list(d)
        self.assertListEqual([], l)

    def test_simplify(self):
        var = 'X1'
        conditions = defaultdict(list, {'X1': ['(A->F)', '(X3->Y1)', '(X2->F)'], 'X2': ['(X1->(B->C))']})
        new_vars = simplify(var, conditions)
        self.assertDictEqual({'X2': ['A', 'X3', '((X2->F)->(B->C))'], 'X3': ['A', 'X2'], 'X1': ['(X2->F)'], 'Y1': ['F']},
                             conditions)
        self.assertSetEqual(set(new_vars), set(['X3', 'Y1']))

    def test_resolve_conditions(self):
        conditions = defaultdict(list, {'X2': ['(X1->B)', '(A->B)'], 'X3': ['(X4->X1)', '(X5->A)'], 'X4': ['C'], 'X6': ['(X1->X3)']})
        self.assertDictEqual({'X1': ['A'], 'X2': ['(A->B)'], 'X3': ['(C->A)'], 'X4': ['C'], 'X5': ['C'], 'X6': ['(A->(C->A))']},
                             resolve_conditions(conditions))

    def test_resolve_conditions2(self):
        conditions = {'X1': ['(X3->A)'], 'X2': ['(X4->A)']}
        print(resolve_conditions(conditions))