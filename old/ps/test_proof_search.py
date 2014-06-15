import unittest

from formula import Formula
from old.ps.proof_search import ProofSearch


class Tests(unittest.TestCase):

    def test_find_in_cs_const(self):
        ps = ProofSearch({'a': ['A', 'B'], 'b': ['A', 'B']})
        f = Formula('(a:A)')
        result = ps.find_in_cs(f.proof_term(), f.subformula())
        self.assertTrue(result)
        self.assertTrue('a:A' in result)

    def test_find_in_cs_const2(self):
        ps = ProofSearch({'a': ['B'], 'b': ['A', 'B']})
        f = Formula('(a:A)')
        result = ps.find_in_cs(f.proof_term(), f.subformula())
        self.assertFalse(result)
        self.assertTrue(result == [])

    def test_find_in_cs_plus1(self):
        ps = ProofSearch({'a': ['C'], 'b': ['A', 'B']})
        f = Formula('((a+b):B)')
        result = ps.find_in_cs(f.proof_term(), f.subformula())
        self.assertTrue(result)
        self.assertTrue('b:B' in result)
        self.assertEqual(len(result), 1)

    def test_find_in_cs_bang1(self):
        ps = ProofSearch({'a': ['B', 'C'], 'b': ['A', 'B']})
        f = Formula('((!a):(a:B))')
        result = ps.find_in_cs(f.proof_term(), f.subformula())
        self.assertTrue(result)
        self.assertTrue('a:B' in result)
        self.assertEqual(len(result), 1)

    def test_find_in_cs_mult1(self):
        ps = ProofSearch({'a': ['(X->F)', '(Y->F)'], 'b': ['Z', 'X']})
        f = Formula('((a*b):F)')
        result = ps.find_in_cs(f.proof_term(), f.subformula())
        self.assertTrue(result)
        self.assertTrue('a:(X->F)' in result)

    # def test_resolve_simple(self):
    #     ps = ProofSearch({})
    #     f = Formula('(a:A)')
    #     ps.resolve(f.proof_term(), f.subformula(), True)

    def test_is_provable_simple1(self):
        ps = ProofSearch({})
        f = Formula('(a:A)')
        result = ps.is_provable(f.proof_term(), f.subformula(), True)
        self.assertFalse(result)

    def test_is_provable_simple2(self):
        print("========================")
        ps = ProofSearch({'a': ['A']})
        f = Formula('(a:A)')
        result = ps.is_provable(f.proof_term(), f.subformula(), True)
        self.assertTrue(result)

    # def test_resolve_plus(self):
    #     ps = ProofSearch({})
    #     f = Formula('((a+b):A)')
    #     self.assertEqual('+', ps.resolve(f.proof_term(), f.subformula(), True))
    #
    # def test_resolve_mult(self):
    #     ps = ProofSearch({})
    #     f = Formula('((a*b):A)')
    #     self.assertEqual('*', ps.resolve(f.proof_term(), f.subformula(), True))
    #     print(str(f))
    #
    # def test_resolve_bang(self):
    #     ps = ProofSearch({})
    #     f = Formula('((!a):A)')
    #     self.assertEqual('!', ps.resolve(f.proof_term(), f.subformula(), True))
    #
    # def test_ultimativ(self):
    #     ps = ProofSearch({})
    #     f = Formula('((((!(a+b))+(d*e))*(!((f+g)*h))):F)')
