import unittest
from formula import Formula
from proof_search import ProofSearch


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
        f = Formula('(!a:(a:B))')
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

    def test_find1(self):
        ps = ProofSearch({'a': ['A', 'B'], 'b': ['A', 'B']})
        f = Formula('(a:A)')
        result = ps.find(f.proof_term(), f.subformula())
        self.assertEqual('(a:A)', result)

    def test_resolve1(self):
        ps = ProofSearch({})
        f = Formula('(a:A)')
        try:
            ps.resolve(f.proof_term(), f.subformula())
        except AssertionError:
            pass
        else:
            self.fail('resolve should not be called if proof_term is const.')

    def test_resolve2(self):
        ps = ProofSearch({})
        f1 = Formula('((a+b):A)')
        f2 = Formula('((a*b):A)')
        f3 = Formula('((!a):A)')
        self.assertEqual('+', ps.resolve(f1.proof_term(), f1.subformula()))
        self.assertEqual('*', ps.resolve(f2.proof_term(), f2.subformula()))
        print(f3.top_operation())
        print(str(f2))
        self.assertEqual('!', ps.resolve(f3.proof_term(), f3.subformula()))

    def test_ultimativ(self):
        ps = ProofSearch({})
        f = Formula('(((!(a+b)+(d*e))*!((f+g)*h)):F')
