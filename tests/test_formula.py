import unittest
from formula import Formula


class Tests(unittest.TestCase):

    def test_init(self):
        f = Formula('(a:F)')
        self.assertEqual('(a:F)', f.formula)
        self.assertEqual(':', f.op)

    def test_proof_term(self):
        f = Formula('(a:F)')
        self.assertEqual('a', f.proof_term().formula)

    def test_subformula(self):
        f = Formula('(a:F)')
        self.assertEqual('F', f.subformula().formula)

    def test_sum_split1(self):
        f = Formula('((a+b):F)')
        self.assertEqual(2, len(f.sum_split()))
        # print(f.sum_split()[0].tree.to_s())
        # print(f.sum_split()[1].tree.to_s())

    def test_sum_split2(self):
        f = Formula('((((f+e)*d)+((!b)+a)):F)')
        self.assertEqual(4, len(f.sum_split()))

    def test_sum_split3(self):
        f = Formula('(((a*b)+(a*b)):F)')
        self.assertEqual(1, len(f.sum_split()))

    def test_remove_bang1(self):
        f = Formula('((!a):(a:A)))')
        self.assertEqual('(a:A)', f.remove_bang().tree.to_s())
        f = Formula('((!((a+b)*c)):(((a+b)*c):F))')
        self.assertEqual('(((a+b)*c):F)', f.remove_bang().tree.to_s())

    def test_remove_bang2(self):
        f = Formula('((!((a+b)*c)):((b*c):F))')
        self.assertIsNone(f.remove_bang())

    def test_to_pieces(self):
        f = Formula('(((!b)+a):(b:X))')
        parts = f.to_pieces()
        self.assertEqual(2, len(parts))
        print(parts[0].tree.to_s())
        print(parts[1].tree.to_s())