import unittest
from helper import *


class Tests(unittest.TestCase):

    def test_wilds(self):
        m = ('a', '(((b:X33)->(X1->(b:F))):X1)')
        keys = wilds(m[1])
        self.assertListEqual(['X1', 'X1', 'X33'], keys)

    def test_unique_wilds(self):
        m = ('a', '(((b:X33)->(X1->(b:F))):X1)')
        keys = unique_wilds(m[1])
        self.assertListEqual(['X1', 'X33'], keys)

    def test_size(self):
        m = [('a', '(X2->(X1->F))'), ('a', '((b:X5)->X2)'),
             ('a', 'X6'), ('b', 'X5'), ('b', '(X3->X1)'), ('c', 'X6->X1')]
        self.assertEqual(6, size(m))
