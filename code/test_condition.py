import unittest
from condition import *


class Tests(unittest.TestCase):
    def test_get_all_wilds(self):
        l = [('X1', '(A->Y2)'), ('Y2', 'X12'), ('A', 'X3')]
        v = get_all_wilds(l)
        self.assertListEqual(['X1', 'X12', 'X3', 'Y2'], v)

    def test_group_by_var(self):
        l = [('X1', '(A->Y2)'), ('Y2', 'X12'), ('A', 'X3')]
        d = group_by_var(l)
        self.assertDictEqual({'X3': ['A'], 'X12': ['Y2'], 'X1': ['(A->Y2)'], 'Y2': ['X12']}, d)

    def test_group_by_var2(self):
        l = [('X1', '(A->B)'), ('X1', '(X3->Y1)'), ('X1', '(X2->B)'), ('X2', '(X1->(B->C))'), ('X3', 'X1'), ('X1', '(X2->F)')]
        d = group_by_var(l)
        #print(d)

    def test_group_by_var3(self):
        l = [('X1', '(X2->A)')]
        d = group_by_var(l)
        self.assertDictEqual({'X2': [], 'X1': ['(X2->A)']}, d)

    def test_simplify(self):
        var = 'X1'
        conditions = defaultdict(list, {'X1': ['(A->F)', '(X3->Y1)', '(X2->F)'], 'X2': ['(X1->(B->C))']})
        simplify(var, conditions)
        self.assertDictEqual({'X2': ['A', 'X3', '((X2->F)->(B->C))'], 'X3': ['A', 'X2'], 'X1': ['(X2->F)'], 'Y1': ['F']},
                             conditions)

    def test_resolve_conditions(self):
        conditions = [('X1', '(A->B)'), ('Y2', 'X1')]
        print(resolve_conditions(conditions))