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
                             merge(['A', 'A', '', '', '', ''], ['', 'A', '', '', 'B', '', '']))

    def test_match2(self):
        self.assertIsNone(merge(['B', '(b:B)', '', '', '', ''], ['', '(B->F)', '', '', 'B', '']))

    def test_match3(self):
        self.assertListEqual(['', 'S'], merge(['', 'S'], ['', '']))

    def test_merge_(self):
        t1 = ['A', 'B', '']
        t2 = ['A', '', 'C']
        self.assertListEqual(['A', 'B', 'C'], merge(t1, t2))