import unittest
from helper import *


class Tests(unittest.TestCase):

    def test_wilds(self):
        m = ('a', '(((b:X33)->(X1->(b:F))):X1)')
        keys = wild_list(m[1])
        self.assertListEqual(['X1', 'X1', 'X33'], keys)

    def test_unique_wilds(self):
        m = ('a', '(((b:X33)->(X1->(b:F))):X1)')
        keys = unique_wilds(m[1])
        self.assertListEqual(['X1', 'X33'], keys)

    def test_size(self):
        m = [('a', '(X2->(X1->F))'), ('a', '((b:X5)->X2)'),
             ('a', 'X6'), ('b', 'X5'), ('b', '(X3->X1)'), ('c', 'X6->X1')]
        self.assertEqual(6, x_size(m))

    def test_size2(self):
        m = [('s', '(X2->X1)'), ('t', 'X2'), ('v', '(X1->F)')]
        self.assertEqual(2, x_size(m))

    def test_match1(self):
        self.assertListEqual(['A', 'A', '', '', 'B', ''],
                             simple_merge(['A', 'A', '', '', '', ''], ['', 'A', '', '', 'B', '', '']))

    def test_match2(self):
        self.assertIsNone(simple_merge(['B', '(b:B)', '', '', '', ''], ['', '(B->F)', '', '', 'B', '']))

    def test_match3(self):
        self.assertListEqual(['', 'S'], simple_merge(['', 'S'], ['', '']))

    def test_merge_(self):
        t1 = ['A', 'B', '']
        t2 = ['A', '', 'C']
        self.assertListEqual(['A', 'B', 'C'], simple_merge(t1, t2))

    def test_merge2(self):
        self.assertEqual(['(A->B)', '', 'B'], simple_merge(['(A->B)', '', 'B'], ['(A->B)', '', 'B']))

    def test_conditions_to_dict(self):
        a, b = [('X1', 'A'), ('X2', 'D'), ('X1', 'C')], [('X2', 'D'), ('X1', 'B'), ('X2', 'C')]
        merged = conditions_to_dict(a, b)
        self.assertDictEqual({'X1': ['A', 'C', 'B'], 'X2': ['D', 'D', 'C']}, merged)

    def test_config_to_table(self):
        configs = [({'X1': 'A', 'X2': 'B'}, []), ({'X1': '(A->B)', 'X4': 'C'}, [])]
        self.assertListEqual([(['A', 'B', '', ''], []), (['(A->B)', '', '', 'C'], [])],
                             configs_to_table(configs, 4))

    def test_config_to_table2(self):
        # test for no wilds & no condition
        configs = []
        self.assertListEqual([(['', '', ''], [])], configs_to_table(configs, 3))

    def test_config_to_table3(self):
        configs = [({}, [('X1', '(Y2->X2)')])]
        self.assertListEqual([(['', ''], [('X1', '(Y2->X2)')])], configs_to_table(configs, 2))

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

    def test_update_condition_with_x(self):
        list = ['Q', '', '(A->B)']
        term = '(X1->(X2->X3))'
        self.assertEqual('(Q->(X2->(A->B)))', update_condition_with_x(term, list))

    def test_rename_dict_from_x_to_y_wilds(self):
        self.assertDictEqual(rename_dict_from_x_to_y_wilds({'X1': 'bla', 'X2': 'blubb'}), {'Y1': 'bla', 'Y2': 'blubb'})