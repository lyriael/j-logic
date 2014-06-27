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
        # for g in f.sum_split():
        #     print(g.formula)

    def test_sum_split3(self):
        f = Formula('(((a*b)+(a*b)):F)')
        self.assertEqual(1, len(f.sum_split()))

    def test_sum_split4(self):
        f = Formula('((e*(f+g)):F)')
        self.assertEqual(2, len(f.sum_split()))
        s = []
        for term in f.sum_split():
            s.append(term.formula)
        self.assertListEqual(['((e*f):F)', '((e*g):F)'], sorted(s))

    def test_sum_split5(self):
        monster = Formula('(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)')
        many_formulas = monster.sum_split()
        a = []
        for f in many_formulas:
            a.append(f.formula)
        self.assertListEqual(['((!((!a)*(c*(!d)))):F)', '((!(b*(c*(!d)))):F)', '((e*f):F)', '((e*g):F)'], sorted(a))

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
        # print(parts[0].tree.to_s())
        # print(parts[1].tree.to_s())

    def test_get_terms_to_proof(self):
        # real testing on this method should be made in Tree for .proof_terms()
        t = Formula('(((a*(b*c))*(!(d*(!e)))):F)')
        c = t.get_terms_to_proof()
        self.assertListEqual([('a', '(X5->(((d*(!e)):X2)->F))'), ('b', '(X6->X5)'), ('c', 'X6'), ('d', '((e:X4)->X2)'), ('e', 'X4')], c)

    def test_to_pieces_and_get_terms_to_proof(self):
        monster = Formula('(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)')
        parts = monster.to_pieces()
        alle = {}
        for f in parts:
            alle[f.formula] = f.get_terms_to_proof()
        self.assertDictEqual({'((e*f):F)': [('e', '(X1->F)'), ('f', 'X1')],
                              '((e*g):F)': [('e', '(X1->F)'), ('g', 'X1')]}, alle)

    def test_to_pieces_and_get_terms_to_proof2(self):
        yig = Formula('(((!(a*b))+(c*((!d)+e))):((a*b):F))')
        parts = yig.to_pieces()
        tuti = {}
        for f in parts:
            tuti[f.formula] = f.get_terms_to_proof()
        self.assertDictEqual({'((c*e):((a*b):F))': [('c', '(X1->((a*b):F))'), ('e', 'X1')],
                              '((c*(!d)):((a*b):F))': [('c', '((d:X2)->((a*b):F))'), ('d', 'X2')],
                              '((a*b):F)': [('a', '(X1->F)'), ('b', 'X1')]}, tuti)