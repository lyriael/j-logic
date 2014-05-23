import unittest
from helper import *
from tree_node import Node
from formula import Formula
from proof_search import ProofSearch

class Tests(unittest.TestCase):

    def test_parse_string1(self):
        l = parse('(a:A)')
        self.assertListEqual(l, ['(', 'a', ':', 'A', ')'])

    def test_parse_string2(self):
        l = parse('(a:X1)')
        self.assertListEqual(l, ['(', 'a', ':', 'X1', ')'])

    def test_parse_string3(self):
        l = parse('(a:(A->B))')
        self.assertListEqual(l, ['(', 'a', ':', '(', 'A', '->', 'B', ')', ')'])

    def test_parse_string4(self):
        l = parse('(!a:(A->X22))')
        self.assertListEqual(l, ['(', '!', 'a', ':', '(', 'A', '->', 'X22', ')', ')'])

    def test_make_tree1(self):
        r = Node.make_tree('(a:A)')
        self.assertEqual(r.token(), ':')
        self.assertEqual(r.left().token(), 'a')
        self.assertEqual(r.right().token(), 'A')

    def test_make_tree2(self):
        r = Node.make_tree('(!a:(A->X22))')
        self.assertEqual(r.token(), ':')
        self.assertEqual(r.right().token(), '->')
        self.assertEqual(r.left().token(), '!')
        self.assertIsNone(r.left().left())
        self.assertEqual(r.right().right().token(), 'X22')

    def test_implication_matcher1(self):
        cs = {'a': ['(X1->F)'], 'b': ['X1']}
        matches = Formula.match_for_implication(cs['a'], 'F')
        self.assertListEqual(matches, ['X1'])

    def test_implication_matcher2(self):
        cs = {'a': ['(X1->A)'], 'b': ['X1']}
        matches = Formula.match_for_implication(cs['a'], 'F')
        self.assertListEqual(matches, [])

    def test_implication_matcher3(self):
        cs = {'a': ['((X1->X2)->F)', '(X1->F)', '(X2->G)', '(X2->F)'], 'b': ['X1']}
        matches = Formula.match_for_implication(cs['a'], 'F')
        self.assertListEqual(matches, ['(X1->X2)', 'X1', 'X2'])

    def test_formula_mult1(self):
        cs = {'a': ['(X1->F)'], 'b': ['X1']}
        formula = Formula('((a*b):F)')
        self.assertTrue(formula.is_provable(cs))

    def test_formula_mult2(self):
        cs = {'a': ['(X1->F)'], 'b': ['X']}
        formula = Formula('((a*b):F)')
        self.assertFalse(formula.is_provable(cs))

    def test_formula_mult3(self):
        cs = {'a': ['(X->G)', '(Y->F)'], 'b': ['X']}
        formula = Formula('((a*b):F)')
        self.assertFalse(formula.is_provable(cs))

    # def test_formula_mult4(self):
    #     cs = {'l': ['(X1->F)'], 'r': ['X']}
    #     formula = Formula('((!l*r):F)')
    #     self.assertFalse(formula.is_provable(cs))

    # def test_formula_mult5(self):
    #     cs = {'l': ['(X->F)'], 'r': ['X']}
    #     formula = Formula('((!l*r):F)')
    #     self.assertFalse(formula.is_provable(cs))

    # def test_formula_mult2(self):
    #     formula = Formula('((a*(b*c)):F)')
    #     cs = {'a': ['(A->F)', '(A->G)', '(B->F)'], 'b': ['(C->B)'], 'c': ['C']}
    #     self.assertTrue(formula.is_provable(cs))

    # # for later
    # def test_formula_mult2(self):
    #     cs = {'a': ['(X1->H)'], 'b': ['(A->F)', '(B->F)'], 'c': ['C', 'B']}
    #     formula = Formula('(((a+b)*c):F)')
    #     self.assertTrue(formula.is_provable(cs))

    def test_formula_operation1(self):
        formula = Formula('(a:A)')
        self.assertEqual(formula.operation(), '')

    def test_formula_operation2(self):
        formula = Formula('((a+b):A)')
        self.assertEqual(formula.operation(), '+')

    def test_formula_operation3(self):
        formula = Formula('(!a:A)')
        self.assertEqual(formula.operation(), '!')

    def test_formula_operation(self):
        formula = Formula('((!a*(b+c)):A)')
        self.assertEqual(formula.operation(), '*')

    def test_find_in_cs_const(self):
        ps = ProofSearch('(a:A)', {'a': ['A', 'B'], 'b': ['A', 'B']})
        result = ps.find_in_cs(ps._formula.proof_term(), ps._formula.subformula())
        self.assertEqual('(a:A)', result)