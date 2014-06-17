import unittest

from formula import Formula
from proof_search import ProofSearch
from stack import Stack


class Tests(unittest.TestCase):

    def test_const1(self):
        ps = ProofSearch({'a': 'A'}, '(a:A)')
        result = ps.is_provable()
        self.assertTrue(result)

    def test_const2(self):
        ps = ProofSearch({}, '(a:A)')
        result = ps.is_provable()
        self.assertFalse(result)

    def test_wander1(self):
        ps = ProofSearch({}, '')
        s = Stack()
        ps._wander(s, Formula('((a+b)*c)'))
        self.assertEqual('(a*c)', str(s.peek()))