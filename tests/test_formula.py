import unittest
from formula import Formula


class Tests(unittest.TestCase):

    def test_init(self):
        f = Formula('(a:F)')
        self.assertEqual('(a:F)', f.formula)
        self.assertEqual(':', f.op)

    def test_to_pieces_part(self):
        f = Formula('((a+b):F)')
        self.assertEqual(2, len(f.to_pieces()))
        print(f.to_pieces()[0].tree.to_s())
        print(f.to_pieces()[1].tree.to_s())

    # def test_to_pieces(self):
    #     f = Formula('((a+b):F)')
    #     p = f.to_pieces()
    #     self.assertEqual(2, len(p))
    #     self.assertEqual('(a:F)', p[0].formula)