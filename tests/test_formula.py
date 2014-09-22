import unittest
from formula import Formula


class Tests(unittest.TestCase):

    def test_init(self):
        f = Formula('(a:F)')
        self.assertEqual('(a:F)', f.formula)
        self.assertEqual(':', f._tree.root.token)

    def test_sum_split1(self):
        f = Formula('((a+b):F)')
        self.assertEqual(2, len(f._sum_split()))
        # print(f.sum_split()[0].tree.to_s())
        # print(f.sum_split()[1].tree.to_s())

    def test_sum_split2(self):
        f = Formula('((((f+e)*d)+((!b)+a)):F)')
        self.assertEqual(4, len(f._sum_split()))
        # for g in f.sum_split():
        #     print(g.formula)

    def test_sum_split3(self):
        f = Formula('(((a*b)+(a*b)):F)')
        self.assertEqual(1, len(f._sum_split()))

    def test_sum_split4(self):
        f = Formula('((e*(f+g)):F)')
        self.assertEqual(2, len(f._sum_split()))
        s = []
        for term in f._sum_split():
            s.append(term.formula)
        self.assertListEqual(['((e*f):F)', '((e*g):F)'], sorted(s))

    def test_sum_split5(self):
        monster = Formula('(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)')
        many_formulas = monster._sum_split()
        a = []
        for f in many_formulas:
            a.append(f.formula)
        self.assertListEqual(['((!((!a)*(c*(!d)))):F)', '((!(b*(c*(!d)))):F)',
                              '((e*f):F)', '((e*g):F)'], sorted(a))

    def test_remove_bang1(self):
        f = Formula('((!a):(a:A)))')
        self.assertEqual('(a:A)', f._simplify_bang()._tree.to_s())
        f = Formula('((!((a+b)*c)):(((a+b)*c):F))')
        self.assertEqual('(((a+b)*c):F)', f._simplify_bang()._tree.to_s())

    def test_remove_bang2(self):
        f = Formula('((!((a+b)*c)):((b*c):F))')
        self.assertIsNone(f._simplify_bang())

    def test_to_pieces(self):
        f = Formula('(((!b)+a):(b:X))')
        parts = f.atomize()
        self.assertEqual(2, len(parts))
        # print(parts[0].tree.to_s())
        # print(parts[1].tree.to_s())

    def test_get_terms_to_proof(self):
        # real testing on this method should be made in Tree for .proof_terms()
        t = Formula('(((a*(b*c))*(!(d*(!e)))):F)')
        c = t.look_ups()
        self.assertListEqual([('a', '(X5->(((d*(!e)):X2)->F))'), ('b', '(X6->X5)'),
                              ('c', 'X6'), ('d', '((e:X4)->X2)'), ('e', 'X4')], c)