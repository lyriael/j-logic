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
        self.assertEqual(6, size(m))

    def test_size2(self):
        m = [('s', '(X2->X1)'), ('t', 'X2'), ('v', '(X1->F)')]
        self.assertEqual(2, size(m))

    def test_match1(self):
        self.assertListEqual(['A', 'A', '', '', 'B', ''],
                             merge(['A', 'A', '', '', '', ''], ['', 'A', '', '', 'B', '', '']))

    def test_match2(self):
        self.assertIsNone(merge(['B', '(b:B)', '', '', '', ''], ['', '(B->F)', '', '', 'B', '']))

    def test_match3(self):
        self.assertListEqual(['', 'S'], merge(['', 'S'], ['', '']))

    def test_config_to_table(self):
        configs = [{'X1': 'A', 'X2': 'B'}, {'X1': '(A->B)', 'X4': 'C'}]
        print(configs_to_table(configs, 4))

    def test_y_to_x1(self):
        wilds_y = {'Y1': ['X3', '(X1->F)'], 'Y2': ['X2']}
        self.assertDictEqual({'X3': '(X1->F)'}, y_to_x(wilds_y))

    def test_y_to_x2(self):
        wilds_y = {'Y1': ['X3', 'X2', '(X1->F)']}
        self.assertDictEqual({'X3': '(X1->F)', 'X2': '(X1->F)'}, y_to_x(wilds_y))

    def test_y_to_x3(self):
        wilds_y = {'Y1': ['(A->B)', 'A']}
        self.assertFalse(y_to_x(wilds_y))

    def test_y_to_x4(self):
        self.assertDictEqual({}, y_to_x({'Y1': ['X1'], 'Y2': ['X2'], 'Y3': ['F']}))

    def test_y_to_x5(self):
        self.assertDictEqual({'X1': 'F'}, y_to_x({'Y1': ['X1', 'F']}))
