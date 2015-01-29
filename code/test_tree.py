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

    def test_unify(self):
        self.assertIsNone(unify('(X1->(c:F))', '(Y1->(Y2->Y3))'))
        self.assertIsNone(unify('(A->B)', '((X1->X2)->X3)'))
        self.assertDictEqual({'X1': ['(A->B)'], 'X2': ['C']}, unify('(X1->X2)', '((A->B)->C)'))
        self.assertDictEqual({'Y1': ['(X1->X2)'], 'Y2': ['X3'], 'X3': ['Y2']}, unify('(Y1->Y2)', '((X1->X2)->X3)'))
        self.assertDictEqual({'Y1': ['(X1->F)', 'X3'], 'X2': ['Y2'], 'Y2': ['X2'], 'X3': ['Y1']},
                             unify('(X3->(X2->(X1->F)))', '(Y1->(Y2->Y1))'))
        self.assertDictEqual({'Y1': ['(X1->F)', 'X2', 'X3'], 'X2': ['Y1'], 'X3': ['Y1']},
                             unify('(X3->(X2->(X1->F)))', '(Y1->(Y1->Y1))'))
        self.assertDictEqual({'X2': ['Y1'], 'Y1': ['X2', 'X1', 'B'], 'X1': ['Y1']},
                             unify('(X1->(B->X2))', '(Y1->(Y1->Y1))'))
        self.assertDictEqual({'X2': ['(Y1->F)'], 'Y1': ['X1'], 'X1': ['Y1']}, unify('(X1->X2)', '(Y1->(Y1->F))'))
        self.assertDictEqual({'X2': ['(Y2->F)'], 'Y1': ['X1'], 'X1': ['Y1']}, unify('(X1->X2)', '(Y1->(Y2->F))'))
        self.assertDictEqual({'X2': ['(Y2->F)'], 'X3': ['(Y1->G)'], 'X1': ['Y1'], 'Y1': ['X1']},
                             unify('((X1->X2)->X3)', '((Y1->(Y2->F))->(Y1->G))'))
        self.assertDictEqual({'X2': ['(Y2->F)'], 'X3': ['(Y2->G)'], 'X1': ['Y1'], 'Y1': ['X1']},
                             unify('((X1->X2)->X3)', '((Y1->(Y2->F))->(Y2->G))'))
        self.assertDictEqual({'Y1': ['(X1->F)', 'X2'], 'X2': ['Y1'], 'X3': ['(Y1->Y2)']},
                             unify('(X3->(X2->(X1->F)))', '((Y1->Y2)->(Y1->Y1))'))
        self.assertDictEqual({'X2': ['Y1'], 'Y1': ['X2'], 'X1': ['(Y2->Y1)']}, unify('(X2->X1)', '(Y1->(Y2->Y1)'))
        self.assertDictEqual({'Y1': ['(X2->G)', '(X1->F)'], 'Y2': ['B']},
                             unify('((X1->F)->(B->(X2->G)))', '(Y1->(Y2->Y1)'))
        self.assertDictEqual({'X3': ['Y1'], 'Y1': ['(X1->F)', 'X3'], 'Y2': ['(a:X2)']},
                             unify('(X3->((a:X2)->(X1->F)))', '(Y1->(Y2->Y1))'))
        self.assertDictEqual({'X1': ['(Y1->Y2)']}, unify('(Y1->Y2)', 'X1'))
        self.assertDictEqual({'Y1': ['X3', 'F'], 'X2': ['Y2'], 'Y2': ['X2'], 'X3': ['Y1']},
                             unify('(Y1->(Y2->Y1))', '(X3->(X2->F))'))

    def test_sum_split1(self):
        self.assertEqual(2, len(Tree.sum_split('((a+b):F)')))
        self.assertEqual(4, len(Tree.sum_split('((((f+e)*d)+((!b)+a)):F)')))
        self.assertEqual(1, len(Tree.sum_split('(((a*b)+(a*b)):F)')))
        self.assertEqual(2, len(Tree.sum_split('((e*(f+g)):F)')))

    def test_sum_split2(self):
        s = []
        for term in Tree.sum_split('((e*(f+g)):F)'):
            s.append(term)
        self.assertListEqual(['((e*f):F)', '((e*g):F)'], sorted(s))

    def test_sum_split3(self):
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

    def test_resolve_conditions3(self):
        conditions = defaultdict(list, {'Y1': ['X3', 'F'], 'X2': ['Y2'], 'Y2': ['X2'], 'X3': ['Y1']})
        self.assertDictEqual({'Y1': ['F'], 'X2': ['X2'], 'Y2': ['X2'], 'X3': ['F']}, resolve_conditions(conditions))

    def test_simplify2(self):
        var = 'Y1'
        conditions = defaultdict(list, {'Y1': ['X3', 'F'], 'X2': ['Y2'], 'Y2': ['X2'], 'X3': ['Y1']})

