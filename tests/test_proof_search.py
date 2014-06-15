import unittest

from formula import Formula
from proof_search import ProofSearch


class Tests(unittest.TestCase):

    def test_init(self):
        ps = ProofSearch({}, '((a+b):F)')
        self.assertDictEqual({'F': ['(a+b)']}, ps._to_proof)

    def test_get_ready(self):
        ps = ProofSearch({}, '((a+b):F)')
        ps.get_ready()
        self.assertDictEqual({'F': ['a', 'b']}, ps._to_proof)

    def test_const1(self):
        ps = ProofSearch({'a': 'A'}, '(a:A)')
        result = ps.is_provable()
        self.assertTrue(result)

    def test_const2(self):
        ps = ProofSearch({}, '(a:A)')
        result = ps.is_provable()
        self.assertFalse(result)

    # def test_plus1(self):
    #     ps = ProofSearch({'a': 'A'})
    #     f = Formula('((b+a):A)')
    #     result = ps.is_provable(f)
    #     self.assertTrue(result)