import unittest
from formula import Formula


class Tests(unittest.TestCase):

    def test_init(self):
        f = Formula('(a:F)')
        self.assertEqual('(a:F)', f.formula)
        self.assertEqual(':', f._tree.root.token)



    def test_to_pieces(self):
        f = Formula('(((!b)+a):(b:X))')
        parts = f.atomize()
        self.assertEqual(2, len(parts))
        # print(parts[0].tree.to_s())
        # print(parts[1].tree.to_s())

    def test_get_terms_to_proof(self):
        # real testing on this method should be made in Tree for .proof_terms()
        t = Formula('(((a*(b*c))*(!(d*(!e)))):F)')
        c = t.get_musts()
        self.assertListEqual([('a', '(X5->(((d*(!e)):X2)->F))'), ('b', '(X6->X5)'),
                              ('c', 'X6'), ('d', '((e:X4)->X2)'), ('e', 'X4')], c)