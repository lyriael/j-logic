import unittest
from formula import Formula
from proof_search import ProofSearch


class Tests(unittest.TestCase):

    def test_find_in_cs_const(self):
        ps = ProofSearch('(a:A)', {'a': ['A', 'B'], 'b': ['A', 'B']})
        result = ps.find_in_cs(ps._formula.proof_term(), ps._formula.subformula())
        self.assertTrue(result)
        self.assertTrue('a:A' in result)

    def test_find_in_cs_const2(self):
        ps = ProofSearch('(a:A)', {'a': ['B'], 'b': ['A', 'B']})
        result = ps.find_in_cs(ps._formula.proof_term(), ps._formula.subformula())
        self.assertFalse(result)
        self.assertTrue(result == [])

    def test_find_in_cs_plus1(self):
        ps = ProofSearch('((a+b):B)',  {'a': ['C'], 'b': ['A', 'B']})
        result = ps.find_in_cs(ps._formula.proof_term(), ps._formula.subformula())
        self.assertTrue(result)
        self.assertTrue('b:B' in result)
        self.assertEqual(len(result), 1)

    def test_find_in_cs_bang1(self):
        ps = ProofSearch('(!a:(a:B))',  {'a': ['B', 'C'], 'b': ['A', 'B']})
        result = ps.find_in_cs(ps._formula.proof_term(), ps._formula.subformula())
        self.assertTrue(result)
        self.assertTrue('a:B' in result)
        self.assertEqual(len(result), 1)

    def test_find_in_cs_mult1(self):
        ps = ProofSearch('((a*b):F)', {'a': ['(X->F)', '(Y->F)'], 'b': ['Z', 'X']})
        result = ps.find_in_cs(ps._formula.proof_term(), ps._formula.subformula())
        self.assertTrue(result)
        self.assertTrue('a:(X->F)' in result)