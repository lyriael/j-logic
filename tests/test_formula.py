import unittest
from formula import Formula


class Tests(unittest.TestCase):

    def test_init1(self):
        formula1 = Formula('((a+(b*c)):F)')
        formula2 = Formula(formula1)
        self.assertNotEqual(formula1, formula2)
        self.assertEqual(formula1.to_s(), formula2.to_s())
        formula3 = Formula(formula1.proof_term())
        formula4 = Formula('(a+(b*c))')
        self.assertNotEqual(formula3, formula4)
        self.assertEqual(formula1.to_s(), formula2.to_s())

    def test_init2(self):
        formula = Formula('((!a):A)')
        self.assertEqual('((!a):A)', formula.to_s())

    def test_init3(self):
        formula = Formula('((!a):(a:B))')
        self.assertEqual('((!a):(a:B))', formula.to_s())
        self.assertEqual(6, len(formula._tree))
        self.assertEqual(2, len(formula.proof_term()._tree))
        self.assertEqual(3, len(formula.subformula()._tree))

    def test_parts1(self):
        formula = Formula('((a+(b*c)):F)')
        self.assertEqual('(a+(b*c))', formula.proof_term().to_s())
        self.assertEqual('F', formula.subformula().to_s())
        self.assertNotEqual(Formula.parts_to_formula(formula.proof_term(), formula.subformula()), formula)
        self.assertEqual(Formula.parts_to_formula(formula.proof_term(), formula.subformula()).to_s(), formula.to_s())

    def test_top_operation1(self):
        formula = Formula('((a+(b*c)):F)')
        self.assertTrue(formula.top_operation() == ':')
        self.assertIsNone(formula.subformula().top_operation())
        self.assertTrue(formula.proof_term().top_operation() == '+')
