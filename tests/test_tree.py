import unittest
from tree import Tree
from tree import get_all_with_y
from tree import update_y

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

    def test_mismatch_search2(self):
        c = Tree('((A->B)->C)')
        x = Tree('((X1->X2)->X1)')
        y = Tree('((Y1->Y2)->Y1)')
        mismatch, wilds = Tree._mismatch_search(x.root, c.root)
        # self.assertListEqual([], mismatch)
        # self.assertListEqual([('X1', 'A'), ('X2', 'B'), ('X3', 'C')], wilds)
        # mismatch, wilds = Tree._mismatch_search(y.root, c.root)

    # def test_compare_to1(self):
    #     a = Tree('((A->B)->C)')
    #     x = Tree('(X1->X2)')
    #     self.assertDictEqual(x.compare_to(a), {'X1': '(A->B)', 'X2': 'C'})
    #
    # def test_compare_to2(self):
    #     a = Tree('((A->B)->C)')
    #     y = Tree('(Y1->Y2)')
    #     self.assertTrue(y.compare_to(a))
    #
    # def test_compare_to3(self):
    #     y = Tree('(Y1->Y2)')
    #     x = Tree('((X1->X2)->X3)')
    #     self.assertTrue(y.compare_to(x))
    #
    # def test_compare_to4(self):
    #     a = Tree('(A->B)')
    #     x = Tree('(X1->(X2->X3))')
    #     self.assertFalse(x.compare_to(a))
    #
    # def test_compare_to5(self):
    #     y = Tree('(Y1->(Y2->Y1))')
    #     x = Tree('(X3->(X2->(X1->F)))')
    #     self.assertTrue(y.compare_to(x))
    #
    # def test_compare_to6(self):
    #     y = Tree('(Y1->(Y1->Y1))')
    #     x = Tree('(X3->(X2->(X1->F)))')
    #     self.assertTrue(y.compare_to(x))
    #
    # def test_compare_to7(self):
    #     y = Tree('(Y1->Y1)')
    #     a = Tree('((A->B)->A)')
    #     self.assertFalse(y.compare_to(a))
    #
    # def test_compare_to8(self):
    #     y = Tree('(Y1->(Y2->Y1))')
    #     x = Tree('((X1->F)->(B->(X2->G)))')
    #     self.assertTrue(y.compare_to(x))

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
        print(con)
        print(wil)
        self.assertListEqual(con, [('X2', '(X1->F)')])
        self.assertDictEqual(wil, {})

    def test_compare_second_try11(self):
        # hopefully this will never be possible!
        # todo: what to do in this situation?
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
        #todo: __nicer__ would be [('X3', '(X1->Y2)'), ('X2', '(X1->F)')]
        self.assertDictEqual(wil, {})

    def test_apply_condition(self):
        wild = ['A', 'B', '']
        con = ('X1', 'A')
        result, delete = Tree.apply_condition(wild, con)
        self.assertListEqual(wild, result)
        self.assertTrue(delete)

    def test_apply_condition2(self):
        wild = ['A', 'B', '']
        con = ('X1', 'B')
        result, delete = Tree.apply_condition(wild, con)
        self.assertIsNone(result)
        self.assertIsNone(delete)

    def test_apply_condition3(self):
        wild = ['A', 'B', '']
        con = ('X3', 'C')
        result, delete = Tree.apply_condition(wild, con)
        self.assertListEqual(['A', 'B', 'C'], result)
        self.assertTrue(delete)

    def test_apply_condition6(self):
        given = ['(A->F)', 'A']
        con = ('X1', '(X2->F)')
        result, delete = Tree.apply_condition(given, con)
        self.assertListEqual(given, result)
        self.assertTrue(delete)

    def test_apply_condition7(self):
        given = ['(B->(A->F))', 'A', '']
        con = ('X1', '(X3->(X2->F))')
        result, delete = Tree.apply_condition(given, con)
        self.assertListEqual(['(B->(A->F))', 'A', 'B'], result)
        self.assertTrue(delete)

    def test_apply_condition8(self):
        given = ['(B->(A->F))', 'A', 'C']
        con = ('X1', '(X3->(X2->F))')
        result, delete = Tree.apply_condition(given, con)
        self.assertIsNone(result)
        self.assertIsNone(delete)

    def test_apply_condition4(self):
        wild = ['', 'B', '']
        con = ('X1', 'X3')
        result, delete = Tree.apply_condition(wild, con)
        print(result)
        print(delete)
        self.assertListEqual(wild, result)
        self.assertFalse(delete)

    def test_apply_condition5(self):
        wild = ['A', 'B', '']
        con = ('X1', 'X3')
        result, delete = Tree.apply_condition(wild, con)
        self.assertListEqual(['A', 'B', 'A'], result)
        self.assertTrue(delete)

    def test_apply_condition9(self):
        wild = ['', 'B', 'C']
        con = ('X1', '(X2->X3)')
        result, delete = Tree.apply_condition(wild, con)
        self.assertListEqual(['(B->C)', 'B', 'C'], result)
        self.assertTrue(delete)

    def test_apply_condition10(self):
        wild = ['', 'B', '']
        con = ('X1', '(X2->X3)')
        result, delete = Tree.apply_condition(wild, con)
        self.assertListEqual(['', 'B', ''], result)
        self.assertFalse(delete)

    def test_apply_condition11(self):
        wild = ['', 'B', '']
        con = ('X1', '(Y2->F)')
        result, delete = Tree.apply_condition(wild, con)
        self.assertListEqual(['', 'B', ''], result)
        self.assertFalse(delete)

    def test_apply_condition12(self):
        wild = ['(B->F)', '', '']
        con = ('X1', '(Y2->F)')
        result, delete = Tree.apply_condition(wild, con)
        self.assertListEqual(['(B->F)', '', ''], result)
        self.assertDictEqual({'Y2': 'B'}, delete)

    def test_apply_condition13(self):
        wild = ['(B->(A->B))', '', '']
        con = ('X1', '(Y1->Y2)')
        result, delete = Tree.apply_condition(wild, con)
        self.assertListEqual(['(B->(A->B))', '', ''], result)
        self.assertDictEqual({'Y1': 'B', 'Y2': '(A->B)'}, delete)

    def test_apply_condition14(self):
        wild = ['B', '', '']
        con = ('X1', '(Y2->F)')
        result, delete = Tree.apply_condition(wild, con)
        self.assertIsNone(result)
        self.assertIsNone(delete)

    def test_get_all_with_y(self):
        result = get_all_with_y([('X2', '(Y1->A)'), ('X1', '(Y2)'), ('X3', '(Y1->Y2)')], ['Y1'])
        self.assertListEqual([('X2', '(Y1->A)'), ('X3', '(Y1->Y2)')], result)

    def test_get_all_with_y2(self):
        result = get_all_with_y([('X2', '(Y1->A)'), ('X1', 'Y2'), ('X3', '(Y1->Y2)')], ['Y2'])
        self.assertListEqual([('X1', 'Y2'), ('X3', '(Y1->Y2)')], result)

    def test_get_all_with_y3(self):
        result = get_all_with_y([('X2', '(Y1->A)'), ('X1', 'Y2'), ('X3', '(Y1->Y2)')], ['Y3'])
        self.assertListEqual([], result)

    def test_update_y(self):
        x = [('X2', '(Y1->A)'), ('X1', 'Y2'), ('X3', '(Y1->Y2)')]
        x = update_y(x, 'Y1', 'F')
        self.assertListEqual([('X2', '(F->A)'), ('X1', 'Y2'), ('X3', '(F->Y2)')], x)

    def test_update_y2(self):
        x = [('X2', '(Y1->A)'), ('X1', 'Y2'), ('X3', '(Y1->Y2)')]
        wilds = {'Y1': 'F', 'Y2': 'G'}
        for entry in wilds:
            x = update_y(x, entry, wilds[entry])
        self.assertListEqual([('X2', '(F->A)'), ('X1', 'G'), ('X3', '(F->G)')], x)

    def test_merge_two_tables(self):
        t1 = [(['A', 'B', ''], [])]
        t2 = [(['A', '', 'C'], [])]
        self.assertListEqual([(['A', 'B', 'C'], [])], Tree.merge_two_tables(t1, t2))