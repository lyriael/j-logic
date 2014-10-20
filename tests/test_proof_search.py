import unittest
from proof_search import ProofSearch
from proof_search import get_all_with_y
from proof_search import update_y
from proof_search import configs_to_table


class Tests(unittest.TestCase):

    def test__conquer_one(self):
        ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X2->(X1->F))'), ('b', 'B')]
        one = ps.conquer_one('test')
        self.assertListEqual([(['A', 'A'], []),
                              (['A', 'C'], []),
                              (['B', '(b:B)'], [])],
                             one)

    def test__conquer_one1(self):
        ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X2->(X1->F))'), ('b', 'C')]
        one = ps.conquer_one('test')
        self.assertIsNone(one)

    def test_conquer_one2(self):
        ps = ProofSearch({'a': ['((b:B)->(C->F))', 'A', '(Y1->(Y2->Y1))']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X3->(X2->F))')]
        self.assertListEqual([(['', 'C', '(b:B)'], []),
                              (['', '', 'F'], [])],
                             ps.conquer_one('test'))

    def test_conquer(self):
        cs = {'s': ['(B->A)'],
              't': ['B'],
              'v': ['(A->F)']}
        formula = '((v*((s*t)+(!u))):F)'
        ps = ProofSearch(cs, formula)
        # so sollte das erste aus must erfüllbar sein, aber nicht das zweite.
        self.assertTrue(ps.conquer())
        self.assertTrue(ps.conquer_one('((v*(s*t)):F)'))
        self.assertFalse(ps.conquer_one('((v*(!u)):F)'))

    def test_apply_condition(self):
        wild = ['A', 'B', '']
        con = ('X1', 'A')
        result, delete = ProofSearch._apply_condition(wild, con)
        self.assertListEqual(wild, result)
        self.assertTrue(delete)

    def test_apply_condition2(self):
        wild = ['A', 'B', '']
        con = ('X1', 'B')
        result, delete = ProofSearch._apply_condition(wild, con)
        self.assertIsNone(result)
        self.assertIsNone(delete)

    def test_apply_condition3(self):
        wild = ['A', 'B', '']
        con = ('X3', 'C')
        result, delete = ProofSearch._apply_condition(wild, con)
        self.assertListEqual(['A', 'B', 'C'], result)
        self.assertTrue(delete)

    def test_apply_condition6(self):
        given = ['(A->F)', 'A']
        con = ('X1', '(X2->F)')
        result, delete = ProofSearch._apply_condition(given, con)
        self.assertListEqual(given, result)
        self.assertTrue(delete)

    def test_apply_condition7(self):
        given = ['(B->(A->F))', 'A', '']
        con = ('X1', '(X3->(X2->F))')
        result, delete = ProofSearch._apply_condition(given, con)
        self.assertListEqual(['(B->(A->F))', 'A', 'B'], result)
        self.assertTrue(delete)

    def test_apply_condition8(self):
        given = ['(B->(A->F))', 'A', 'C']
        con = ('X1', '(X3->(X2->F))')
        result, delete = ProofSearch._apply_condition(given, con)
        self.assertIsNone(result)
        self.assertIsNone(delete)

    def test_apply_condition4(self):
        wild = ['', 'B', '']
        con = ('X1', 'X3')
        result, delete = ProofSearch._apply_condition(wild, con)
        self.assertListEqual(wild, result)
        self.assertFalse(delete)

    def test_apply_condition5(self):
        wild = ['A', 'B', '']
        con = ('X1', 'X3')
        result, delete = ProofSearch._apply_condition(wild, con)
        self.assertListEqual(['A', 'B', 'A'], result)
        self.assertTrue(delete)

    def test_apply_condition9(self):
        wild = ['', 'B', 'C']
        con = ('X1', '(X2->X3)')
        result, delete = ProofSearch._apply_condition(wild, con)
        self.assertListEqual(['(B->C)', 'B', 'C'], result)
        self.assertTrue(delete)

    def test_apply_condition10(self):
        wild = ['', 'B', '']
        con = ('X1', '(X2->X3)')
        result, delete = ProofSearch._apply_condition(wild, con)
        self.assertListEqual(['', 'B', ''], result)
        self.assertFalse(delete)

    def test_apply_condition11(self):
        wild = ['', 'B', '']
        con = ('X1', '(Y2->F)')
        result, delete = ProofSearch._apply_condition(wild, con)
        self.assertListEqual(['', 'B', ''], result)
        self.assertFalse(delete)

    def test_apply_condition12(self):
        wild = ['(B->F)', '', '']
        con = ('X1', '(Y2->F)')
        result, delete = ProofSearch._apply_condition(wild, con)
        self.assertListEqual(['(B->F)', '', ''], result)
        self.assertDictEqual({'Y2': 'B'}, delete)

    def test_apply_condition13(self):
        wild = ['(B->(A->B))', '', '']
        con = ('X1', '(Y1->Y2)')
        result, delete = ProofSearch._apply_condition(wild, con)
        self.assertListEqual(['(B->(A->B))', '', ''], result)
        self.assertDictEqual({'Y1': 'B', 'Y2': '(A->B)'}, delete)

    def test_apply_condition14(self):
        wild = ['B', '', '']
        con = ('X1', '(Y2->F)')
        result, delete = ProofSearch._apply_condition(wild, con)
        self.assertIsNone(result)
        self.assertIsNone(delete)

    def test_get_all_with_y(self):
        result = get_all_with_y([('X2', '(Y1->A)'), ('X1', '(Y2)'), ('X3', '(Y1->Y2)')], ['Y1'])
        self.assertListEqual([('X2', '(Y1->A)'), ('X3', '(Y1->Y2)')], result)

    def test_get_all_with_y2(self):
        result = get_all_with_y([('X2', '(Y1->A)'), ('X1', 'Y2'), ('X3', '(Y1->Y2)')], ['Y2'])
        self.assertListEqual([('X1', 'Y2'), ('X3', '(Y1->Y2)')], result)

    def test_get_all_with_y3(self):
        result = get_all_with_y([('X2', '(Y1->A)'), ('X1', 'Y2'), ('X3', '(Y1->Y2)')], ['Y3'])
        self.assertListEqual([], result)

    def test_update_y(self):
        x = [('X2', '(Y1->A)'), ('X1', 'Y2'), ('X3', '(Y1->Y2)')]
        x = update_y(x, 'Y1', 'F')
        self.assertListEqual([('X2', '(F->A)'), ('X1', 'Y2'), ('X3', '(F->Y2)')], x)

    def test_update_y2(self):
        x = [('X2', '(Y1->A)'), ('X1', 'Y2'), ('X3', '(Y1->Y2)')]
        wilds = {'Y1': 'F', 'Y2': 'G'}
        for entry in wilds:
            x = update_y(x, entry, wilds[entry])
        self.assertListEqual([('X2', '(F->A)'), ('X1', 'G'), ('X3', '(F->G)')], x)

    def test_merge_two_tables(self):
        t1 = [(['A', 'B', ''], [])]
        t2 = [(['A', '', 'C'], [])]
        self.assertListEqual([(['A', 'B', 'C'], [])], ProofSearch.merge_two_tables(t1, t2))

    def test_config_to_table(self):
        configs = [({'X1': 'A', 'X2': 'B'}, []), ({'X1': '(A->B)', 'X4': 'C'}, [])]
        self.assertListEqual([(['A', 'B', '', ''], []), (['(A->B)', '', '', 'C'], [])],
                             configs_to_table(configs, 4))

    def test_config_to_table2(self):
        # test for no wilds & no condition
        configs = []
        self.assertListEqual([(['', '', ''], [])], configs_to_table(configs, 3))

    def test_find_all_for_none(self):
        ps = ProofSearch({'a': [1, 2, 3]}, '')
        match = ps._find_all_for('b', '')
        self.assertIsNone(match)

    def test_find_all_for_list(self):
        cs = ProofSearch({'a': ['(A->B)', 'C', '(C->D)', '((A->B)->C)']}, '')
        orig_term = '(X1->X2)'
        match = cs._find_all_for('a', orig_term)
        self.assertListEqual([({'X2': 'B', 'X1': 'A'}, []), ({'X2': 'D', 'X1': 'C'}, []), ({'X2': 'C', 'X1': '(A->B)'}, [])], match)

    def test_find_all_for_list1(self):
        cs = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']}, '')
        orig_term = '(X2->(X1->F))'
        match = cs._find_all_for('a', orig_term)
        self.assertListEqual([({'X2': 'A',      'X1': 'A'}, []),
                              ({'X2': 'C',      'X1': 'A'}, []),
                              ({'X2': '(b:B)',  'X1': 'B'}, [])],
                             match)

    # mixing Y's and wilds
    def test_find_all_for_list2(self):
        cs = ProofSearch({'a': ['(Y1->(Y2->Y3))', '(Y1->Y2)']}, '')
        orig_term = '(X1->X2)'
        match = cs._find_all_for('a', orig_term)
        # second fits, but needs no wild
        self.assertListEqual([({}, [('X2', '(Y2->Y3)')])], match)

    # mixing Y's and wilds
    def test_find_list3(self):
        orig_term = '(X2->(X1->F))'
        cs = ProofSearch({'a': ['(Y1->(Y2->Y1))'], 'b': ['B']}, '')
        match = cs._find_all_for('a', orig_term)
        self.assertListEqual([({'X2': 'F'}, [])], match)

    def test_find_all_for_exact(self):
        orig_term = '(X1->(X2->X3))'
        cs = ProofSearch({'a': ['(Y1->(Y2->Y3))']}, '')
        match = cs._find_all_for('a', orig_term)
        self.assertListEqual([], match)

    def test_find_all_for_exact2(self):
        orig_term = '(A->B)'
        cs = ProofSearch({'a': ['(A->B)', '(Y1->Y2)']}, '')
        match = cs._find_all_for('a', orig_term)
        self.assertListEqual([], match)

    def test_find_all_for_exact3(self):
        orig_term = '(A->B)'
        cs = ProofSearch({'a': ['(Y1->Y1)']}, '')
        match = cs._find_all_for('a', orig_term)
        self.assertIsNone(match)

    def test_atomize(self):
        f = ProofSearch({}, '(((!b)+a):(b:X))')
        parts = f.atomize()
        self.assertEqual(2, len(parts))

    def test_divide1(self):
        ps = ProofSearch({}, '(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)')
        self.assertDictEqual({'((e*f):F)': [('e', '(X1->F)'), ('f', 'X1')],
                              '((e*g):F)': [('e', '(X1->F)'), ('g', 'X1')]},
                             ps.musts)

    def test_divide2(self):
        ps = ProofSearch({}, '(((!(a*b))+(c*((!d)+e))):((a*b):F))')
        self.assertDictEqual({'((c*e):((a*b):F))': [('c', '(X1->((a*b):F))'), ('e', 'X1')],
                              '((c*(!d)):((a*b):F))': [('c', '((d:X2)->((a*b):F))'), ('d', 'X2')],
                              '((a*b):F)': [('a', '(X1->F)'), ('b', 'X1')]},
                             ps.musts)

    def test_divide3(self):
        ps = ProofSearch({}, '(((a*b)*(!c)):(c:F))')
        terms_to_match = ps.musts['(((a*b)*(!c)):(c:F))']
        self.assertListEqual([('a', '(X3->((c:X2)->(c:F)))'), ('b', 'X3'), ('c', 'X2')], terms_to_match)

    def test_divide4(self):
        ps = ProofSearch({}, '((((((!a)*b)+(c*d))*((!e)+(f+g)))*(h*i)):F)')
        self.assertDictEqual({'((((c*d)*f)*(h*i)):F)': [('c', '(X4->(X3->(X1->F)))'), ('d', 'X4'), ('f', 'X3'),
                                                        ('h', '(X2->X1)'), ('i', 'X2')],
                              '((((c*d)*(!e))*(h*i)):F)': [('c', '(X5->((e:X4)->(X1->F)))'), ('d', 'X5'), ('e', 'X4'),
                                                           ('h', '(X2->X1)'), ('i', 'X2')],
                              '((((c*d)*g)*(h*i)):F)': [('c', '(X4->(X3->(X1->F)))'), ('d', 'X4'), ('g', 'X3'),
                                                        ('h', '(X2->X1)'), ('i', 'X2')]},
                             ps.musts)
