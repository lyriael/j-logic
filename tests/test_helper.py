import unittest
from helper import *


class Tests(unittest.TestCase):

    def test_get_wilds(self):
        m = [('a', '(X1->F)'), ('a', '((b:X33)->(X1->(b:F)))'), ('b', 'X4')]
        keys = get_wilds(m)
        self.assertDictEqual({'X1': [], 'X33': [], 'X4': []}, keys)