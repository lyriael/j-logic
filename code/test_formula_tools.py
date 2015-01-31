import unittest
from formula_tools import *


class Tests(unittest.TestCase):
    def test_unify(self):
        self.assertIsNone(unify('(X1->(c:F))', '(Y1->(Y2->Y3))'))
        self.assertIsNone(unify('(A->B)', '((X1->X2)->X3)'))
        self.assertIsNone(unify('(X1->F)', '(a:X2)'))
        self.assertDictEqual({'X1': {'(A->B)'}, 'X2': {'C'}}, unify('(X1->X2)', '((A->B)->C)'))
        self.assertDictEqual({'Y1': {'(X1->X2)'}, 'Y2': {'X3'}, 'X3': {'Y2'}}, unify('(Y1->Y2)', '((X1->X2)->X3)'))
        self.assertDictEqual({'Y1': {'(X1->F)', 'X3'}, 'X2': {'Y2'}, 'Y2': {'X2'}, 'X3': {'Y1'}},
                             unify('(X3->(X2->(X1->F)))', '(Y1->(Y2->Y1))'))
        self.assertDictEqual({'Y1': {'(X1->F)', 'X2', 'X3'}, 'X2': {'Y1'}, 'X3': {'Y1'}},
                             unify('(X3->(X2->(X1->F)))', '(Y1->(Y1->Y1))'))
        self.assertDictEqual({'X2': {'Y1'}, 'Y1': {'X2', 'X1', 'B'}, 'X1': {'Y1'}},
                             unify('(X1->(B->X2))', '(Y1->(Y1->Y1))'))
        self.assertDictEqual({'X2': {'(Y1->F)'}, 'Y1': {'X1'}, 'X1': {'Y1'}}, unify('(X1->X2)', '(Y1->(Y1->F))'))
        self.assertDictEqual({'X2': {'(Y2->F)'}, 'Y1': {'X1'}, 'X1': {'Y1'}}, unify('(X1->X2)', '(Y1->(Y2->F))'))
        self.assertDictEqual({'X2': {'(Y2->F)'}, 'X3': {'(Y1->G)'}, 'X1': {'Y1'}, 'Y1': {'X1'}},
                             unify('((X1->X2)->X3)', '((Y1->(Y2->F))->(Y1->G))'))
        self.assertDictEqual({'X2': {'(Y2->F)'}, 'X3': {'(Y2->G)'}, 'X1': {'Y1'}, 'Y1': {'X1'}},
                             unify('((X1->X2)->X3)', '((Y1->(Y2->F))->(Y2->G))'))
        self.assertDictEqual({'Y1': {'(X1->F)', 'X2'}, 'X2': {'Y1'}, 'X3': {'(Y1->Y2)'}},
                             unify('(X3->(X2->(X1->F)))', '((Y1->Y2)->(Y1->Y1))'))
        self.assertDictEqual({'X2': {'Y1'}, 'Y1': {'X2'}, 'X1': {'(Y2->Y1)'}}, unify('(X2->X1)', '(Y1->(Y2->Y1)'))
        self.assertDictEqual({'Y1': {'(X2->G)', '(X1->F)'}, 'Y2': {'B'}},
                             unify('((X1->F)->(B->(X2->G)))', '(Y1->(Y2->Y1)'))
        self.assertDictEqual({'X3': {'Y1'}, 'Y1': {'(X1->F)', 'X3'}, 'Y2': {'(a:X2)'}},
                             unify('(X3->((a:X2)->(X1->F)))', '(Y1->(Y2->Y1))'))
        self.assertDictEqual({'X1': {'(Y1->Y2)'}}, unify('(Y1->Y2)', 'X1'))
        self.assertDictEqual({'Y1': {'X3', 'F'}, 'X2': {'Y2'}, 'Y2': {'X2'}, 'X3': {'Y1'}},
                             unify('(Y1->(Y2->Y1))', '(X3->(X2->F))'))

    def test_sum_split1(self):
        self.assertEqual(2, len(sum_split('((a+b):F)')))
        self.assertEqual(4, len(sum_split('((((f+e)*d)+((!b)+a)):F)')))
        self.assertEqual(1, len(sum_split('(((a*b)+(a*b)):F)')))
        self.assertEqual(2, len(sum_split('((e*(f+g)):F)')))

    def test_sum_split2(self):
        s = []
        for term in sum_split('((e*(f+g)):F)'):
            s.append(term)
        self.assertListEqual(['((e*f):F)', '((e*g):F)'], sorted(s))

    def test_sum_split3(self):
        many_formulas = sum_split('(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)')
        a = []
        for f in many_formulas:
            a.append(f)
        self.assertListEqual(['((!((!a)*(c*(!d)))):F)', '((!(b*(c*(!d)))):F)',
                              '((e*f):F)', '((e*g):F)'], sorted(a))

    def test_simplify_introspection(self):
        self.assertEqual('(a:A)', simplify_introspection('((!a):(a:A)))'))
        self.assertEqual('(((a+b)*c):F)', simplify_introspection('((!((a+b)*c)):(((a+b)*c):F))'))
        self.assertIsNone(simplify_introspection('((!((a+b)*c)):((b*c):F))'))
        self.assertEqual('(a:A)', simplify_introspection('(a:A)'))

    def test_condition_list_to_dict(self):
        l = [('X1', '(A->Y2)'), ('Y2', 'X12'), ('A', 'X3')]
        d = condition_list_to_dict(l)
        self.assertDictEqual(defaultdict(set, {'X3': {'A'}, 'X12': {'Y2'}, 'X1': {'(A->Y2)'}, 'Y2': {'X12'}}), d)

    def test_condition_list_to_dict2(self):
        l = [('X1', '(A->B)'), ('X1', '(X3->Y1)'), ('X1', '(X2->B)'), ('X2', '(X1->(B->C))'), ('X3', 'X1'), ('X1', '(X2->F)')]
        d = condition_list_to_dict(l)
        self.assertDictEqual(defaultdict(set, {'X2': {'(X1->(B->C))'}, 'X3': {'X1'}, 'X1': {'(X2->F)', 'X3', '(X2->B)', '(A->B)', '(X3->Y1)'}}), d)

    def test_condition_list_to_dict3(self):
        l = [('X1', '(X2->A)')]
        d = condition_list_to_dict(l)
        #self.assertDictEqual({'X2': [], 'X1': ['(X2->A)']}, d)
        self.assertDictEqual(defaultdict(set, {'X1': {'(X2->A)'}}), d)

    def test_condition_dict_to_list1(self):
        d = {'X1': [], 'X3': ['(X1->F)']}
        l = condition_dict_to_list(d)
        self.assertListEqual([('X3', '(X1->F)')], l)

    def test_condition_dict_to_list2(self):
        d = {'X1': []}
        l = condition_dict_to_list(d)
        self.assertListEqual([], l)

    def test_simplify(self):
        var = 'X1'
        conditions = defaultdict(set, {'X1': {'(A->F)', '(X3->Y1)', '(X2->F)'}, 'X2': {'(X1->(B->C))'}})
        new_vars = simplify(var, conditions)
        self.assertDictEqual(defaultdict(set, {'X2': {'X3', '((A->F)->(B->C))'}, 'Y1': {'F'}, 'X1': {'(A->F)'}, 'X3': {'X2'}}),
                             conditions)
        self.assertSetEqual(set(new_vars), set({'X3', 'Y1'}))

    def test_simplify2(self):
        var = 'Y1'
        conditions = defaultdict(set, {'Y1': {'X3', 'F'}, 'X2': {'Y2'}, 'Y2': {'X2'}, 'X3': {'Y1'}})
        new_vars = simplify(var, conditions)
        self.assertDictEqual(defaultdict(set, {'Y1': {'X3'}, 'X2': {'Y2'}, 'Y2': {'X2'}, 'X3': {'F'}}), conditions)
        self.assertSetEqual(set(new_vars), set([]))

    def test_resolve_conditions(self):
        conditions = defaultdict(set, {'X2': {'(X1->B)', '(A->B)'}, 'X3': {'(X4->X1)', '(X5->A)'}, 'X4': {'C'}, 'X6': {'(X1->X3)'}})
        self.assertDictEqual({'X1': {'A'}, 'X2': {'(A->B)'}, 'X3': {'(C->A)'}, 'X4': {'C'}, 'X5': {'C'}, 'X6': {'(A->(C->A))'}},
                             resolve_conditions(conditions))

    def test_resolve_conditions3(self):
        conditions = defaultdict(set, {'Y1': {'X3', 'F'}, 'X2': {'Y2'}, 'Y2': {'X2'}, 'X3': {'Y1'}})
        self.assertDictEqual({'Y1': {'F'}, 'Y2': {'X2'}, 'X3': {'F'}}, resolve_conditions(conditions))

    def test_has_bad_introspection(self):
        self.assertTrue(has_bad_introspection('(((!a)*b):F)'))
        self.assertTrue(has_bad_introspection('((((!a)*b)*(!c)):F)'))
        self.assertFalse(has_bad_introspection('(((a*(!b))*(!c)):F)'))

    def test_musts(self):
        self.assertListEqual([('a', '(X1->F)'), ('b', 'X1')], musts('((a*b):F)'))
        self.assertListEqual([('a', '(X2->(X1->F))'), ('b', 'X2'), ('c', 'X1')], musts('(((a*b)*c):F)'))
        self.assertListEqual([('a', '((b:X2)->F)'), ('b', 'X2')], musts('((a*(!b)):F)'))
        self.assertListEqual([('a', '(X5->(((d*(!e)):X2)->F))'), ('b', '(X6->X5)'),
                              ('c', 'X6'), ('d', '((e:X4)->X2)'), ('e', 'X4')],
                             musts('(((a*(b*c))*(!(d*(!e)))):F)'))

    def test_merge_dicts(self):
        self.assertDictEqual(defaultdict(set, {'X1': {'a', 'b', 'c'}, 'X2': {'a', 'b'}, 'X3': {'a', 'b', 'c'}}),
                             merge_dicts(defaultdict(set, {'X2': {'a', 'b'}, 'X3': {'a'}}),
                                         defaultdict(set, {'X1': {'a', 'b', 'c'}, 'X2':{'b'}, 'X3': {'b', 'c'}})))
        self.assertDictEqual({'X2': {'B'}, 'X3': {'C'}, 'X1': {'A'}},
                             merge_dicts({'X3': {'C'}}, {'X1': {'A'}, 'X2': {'B'}}))
        self.assertDictEqual({'X1': {'A', 'X3'}, 'X2': {'B'}}, merge_dicts({'X1': {'X3'}}, {'X1': {'A'}, 'X2': {'B'}}))
        self.assertDictEqual({'X1': {'A', 'B'}}, merge_dicts({'X1': {'A', 'B'}}, {}))
        self.assertDictEqual({'X1': {'A', 'B'}}, merge_dicts({}, {'X1': {'A', 'B'}}))

    def test_merge_dicts2(self):
        dict1 = defaultdict(set, {'X2': {'B'}, 'X1': {'A'}})
        dict2 = defaultdict(set, {'X2': {'C'}, 'X1': {'B'}})
        merge_dicts(dict1, dict2)
        self.assertDictEqual(defaultdict(set, {'X2': {'B'}, 'X1': {'A'}}), dict1)
        self.assertDictEqual(defaultdict(set, {'X2': {'C'}, 'X1': {'B'}}), dict2)
