import unittest
from proof_search import *


class Tests(unittest.TestCase):

    def test_conquer_one_atom0(self):
        ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X2->(X1->F))'), ('b', 'C')]
        conditions = ps.conquer_one_atom('test')
        self.assertIsNone(conditions)

    def test_conquer_one_atom1(self):
        ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X2->(X1->F))'), ('b', 'B')]
        self.assertListEqual([defaultdict(list, {'X2': ['A'], 'X1': ['A']}),
                              defaultdict(list, {'X2': ['C'], 'X1': ['A']}),
                              defaultdict(list, {'X2': ['(b:B)'], 'X1': ['B']})],
                             ps.conquer_one_atom('test'))

    def test_conquer_one_atom2(self):
        ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X2->(X1->F))'), ('b', 'C')]
        one = ps.conquer_one_atom('test')
        self.assertIsNone(one)

    def test_conquer_one_atom3(self):
        ps = ProofSearch({'a': ['((b:B)->(C->F))', 'A', '(Y1->(Y2->Y1))']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X3->(X2->F))')]
        self.assertListEqual([defaultdict(list, {'X2': ['C'], 'X3': ['(b:B)']}),
                              defaultdict(list, {'Y1': ['F'], 'X2': ['X2'], 'Y2': ['X2'], 'X3': ['F']})],
                             ps.conquer_one_atom('test'))

    def test_conquer_one_atom4(self):
        self.assertListEqual([{}], ProofSearch({'a': ['F']}, '(a:F)').conquer_one_atom('(a:F)'))

    def test_conquer_one_atom5(self):
        self.assertIsNone(ProofSearch({'a': ['F']}, '(a:G)').conquer_one_atom('(a:G)'))

    def test_conquer_one_atom6(self):
        ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X2->(X1->F)))')]
        self.assertListEqual([defaultdict(list, {'X2': ['A'], 'X1': ['A']}),
                              defaultdict(list, {'X2': ['C'], 'X1': ['A']}),
                              defaultdict(list, {'X2': ['(b:B)'], 'X1': ['B']})],
                             ps.conquer_one_atom('test'))

    def test_conquer_one_atom7(self):
        ps = ProofSearch({'a': ['(Y1->(Y2->Y3))', '(Y1->Y2)']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X1->X2)')]
        self.assertListEqual([defaultdict(list, {'X2': ['(Y2->Y3)'], 'Y1': ['Y1'], 'X1': ['Y1']}),
                              defaultdict(list, {'X2': ['X2'], 'Y1': ['Y1'], 'X1': ['Y1'], 'Y2': ['X2']})],
                             ps.conquer_one_atom('test'))

    def test_conquer_one_atom8(self):
        ps = ProofSearch({'a': ['(Y1->(Y2->Y1))'], 'b': ['B']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X2->(X1->F))')]
        self.assertListEqual([defaultdict(list, {'Y1': ['F'], 'X1': ['X1'], 'Y2': ['X1'], 'X2': ['F']})],
                             ps.conquer_one_atom('test'))

    def test_conquer_one_atom9(self):
        ps = ProofSearch({'a': ['(Y1->(Y2->Y3))'], 'b': ['B']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X1->(X2->X3))')]
        self.assertListEqual([defaultdict(list, {'X1': ['X1'], 'Y1': ['X1'], 'X2': ['X2'],
                                                 'X3': ['X3'], 'Y3': ['X3'], 'Y2': ['X2']})],
                             ps.conquer_one_atom('test'))

    def test_conquer_one_atom10(self):
        ps = ProofSearch({'a': ['(A->B)', '(Y1->Y2)'], 'b': ['B']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(A->B)')]
        self.assertListEqual([{}, defaultdict(list, {'Y1': ['A'], 'Y2': ['B']})],
                             ps.conquer_one_atom('test'))

    def test_conquer_one_atom11(self):
        ps = ProofSearch({'a': ['(Y1->Y1)']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(A->B)')]
        self.assertIsNone(ps.conquer_one_atom('test'))

    def test_conquer_one_atom12(self):
        ps = ProofSearch({'a': ['((c:X3)->X1)']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(G->(H->G))')]
        self.assertIsNone(ps.conquer_one_atom('test'))

    def test_conquer_one_atom13(self):
        ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['C']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X2->(X1->F))')]
        self.assertListEqual([defaultdict(list, {'X2': ['A'], 'X1': ['A']}), defaultdict(list, {'X2': ['C'], 'X1': ['A']}),
                              defaultdict(list, {'X2': ['(b:B)'], 'X1': ['B']})], ps.conquer_one_atom('test'))

    def test_conquer_all_atoms4(self):
        result = ProofSearch({'a': ['F']}, '(a:F)').conquer_all_atoms()
        self.assertTrue(result[0])
        self.assertDictEqual({'(a:F)': []}, result[1])

    def test_conquer_all_atoms5(self):
        result = ProofSearch({'a': ['F']}, '(a:G)').conquer_all_atoms()
        self.assertFalse(result[0])
        self.assertDictEqual({'(a:G)': 'Not provable.'}, result[1])

    def test_resolve_conditions(self):
        self.assertIsNone(resolve_conditions(defaultdict(list, {'X1': ['A', 'B']})))
        self.assertIsNone(resolve_conditions(defaultdict(list, {'X1': ['B', '(Y2->F)']})))
        self.assertIsNone(resolve_conditions(defaultdict(list, {'X1': ['(A->B)', '(Y2->X2)'], 'X2': ['C']})))
        self.assertIsNone(resolve_conditions(defaultdict(list, {'X1': ['(B->(A->F))', '(X3->(X2->F))'],
                                                                'X2': ['A'], 'X3': ['C']})))
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['A', 'X3'], 'X2': ['B']})),
                             {'X1': ['A'], 'X2': ['B'], 'X3': ['A']})
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['(A->F)', '(X2->F)'], 'X2': ['A']})),
                             {'X1': ['(A->F)'], 'X2': ['A']})
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['(B->(A->F))', '(X3->(X2->F))'], 'X2': ['A']})),
                             {'X1': ['(B->(A->F))'], 'X2': ['A'], 'X3': ['B']})
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['(X2->X3)'], 'X2': ['B'], 'X3': ['C']})),
                             {'X1': ['(B->C)'], 'X2': ['B'], 'X3': ['C']})
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['(X2->X3)'], 'X2': ['B']})),
                             {'X1': ['(B->X3)'], 'X2': ['B']})
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['(Y2->F)'], 'X2': ['B']})),
                             {'X1': ['(Y2->F)'], 'X2': ['B']})
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['(B->F)', '(Y2->F)']})),
                             {'X1': ['(B->F)'], 'Y2': ['B']})
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['(B->(A->B))', '(Y1->Y2)']})),
                             {'X1': ['(B->(A->B))'], 'Y2': ['(A->B)'], 'Y1': ['B']})
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['(Y2->X2)'], 'X2': ['B']})),
                             {'X1': ['(Y2->B)'], 'X2': ['B']})
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['(A->B)', '(Y2->X2)']})),
                             {'X1': ['(A->B)'], 'X2': ['B'], 'Y2': ['A']})
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['(A->B)', '(Y2->X2)'], 'X2': ['B']})),
                             {'X1': ['(A->B)'], 'X2': ['B'], 'Y2': ['A']})
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['(A->B)'], 'X2': ['(X3->Y1)'], 'X3': ['B']})),
                             {'X1': ['(A->B)'], 'X2': ['(B->Y1)'], 'X3': ['B']})
        self.assertDictEqual(resolve_conditions(defaultdict(list, {'X1': ['(Y2->X3)', '(A->B)'],
                                                                   'X2': ['C'], 'X3': ['B']})),
                             {'X1': ['(A->B)'], 'X2': ['C'], 'X3': ['B'], 'Y2': ['A']})

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

    def test_combine(self):
        existing = [{'X1':['A'], 'X2':['B']}, {'X1': ['(A->B)'], 'X3': ['C']}]
        new = [{'X1': ['B'], 'X2': ['C']}, {'X1': ['A'], 'X2': ['B']}]
        self.assertListEqual([{'X2': ['B'], 'X1': ['A']}], combine(new, existing))

    def test_combine2(self):
        existing = [{'X1': ['A'], 'X2':['B']}, {'X2': ['(A->B)']}]
        new = [{'X1': ['A'], 'X3': ['C']}]
        self.assertListEqual([{'X3': ['C'], 'X2': ['B'], 'X1': ['A']}, {'X3': ['C'], 'X2': ['(A->B)'], 'X1': ['A']}],
                             combine(new, existing))

    def test_nice(self):
        self.assertListEqual([[('X2', ''), ('X3', 'F')]],
                             nice([{'Y1': ['F'], 'X2': ['X2'], 'Y2': ['X2'], 'X3': ['F']}]))

    def test_conquer_all_atoms1(self):
        cs = defaultdict(list, {'s': ['(B->A)'],
              't': ['B'],
              'v': ['(A->F)']})
        formula = '((v*((s*t)+(!u))):F)'
        ps = ProofSearch(cs, formula)
        result = ps.conquer_all_atoms()
        self.assertTrue(result[0])
        self.assertDictEqual({'((v*(s*t)):F)': [[('X1', 'A'), ('X2', 'B')]],
                              '((v*(!u)):F)': 'Not provable.'},
                             result[1])

    def test_conquer_all_atoms2(self):
        formula = '(((((a*b)*(!b))+((!b)+c))+((!b)*d)):(b:F))'
        cs = {'a': ['(G->((b:B)->(b:F)))', '(Y1->(Y2->Y1))'], 'b': ['(b:F)', 'G']}
        ps = ProofSearch(cs, formula)
        result = ps.conquer_all_atoms()
        self.assertTrue(result[0])
        self.assertDictEqual({'(c:(b:F))': 'Not provable.',
                              '(b:F)': 'Not provable.',
                              '(((a*b)*(!b)):(b:F))': [[('X2', '(b:F)'), ('X3', '(b:F)')],
                                                       [('X2', 'G'), ('X3', '(b:F)')]]},
                             result[1])

    def test_conquer_all_atoms3(self):
        ps = ProofSearch({'a': ['((A->C)->F)'], 'b': ['(Y1->(Y2->Y1))'], 'c': ['C']}, '((a*(b*c)):F)')
        self.assertListEqual([{'Y1': ['C'], 'X2': ['C'], 'X1': ['(A->C)'], 'Y2': ['A']}],
                             ps.conquer_one_atom('((a*(b*c)):F)'))
        result = ps.conquer_all_atoms()
        self.assertTrue(result[0])
        self.assertDictEqual({'((a*(b*c)):F)': [[('X1', '(A->C)'), ('X2', 'C')]]}, result[1])

    def test_merge_dicts(self):
        self.assertDictEqual({'X1': ['a', 'b', 'c'], 'X2': ['a', 'b'], 'X3': ['a', 'b', 'c']},
                             merge_dicts({'X2': ['a', 'b'], 'X3': ['a']},
                                         {'X1': ['a', 'b', 'c'], 'X2':['b'], 'X3': ['b', 'c']}))
        self.assertDictEqual({'X2': ['B'], 'X3': ['C'], 'X1': ['A']},
                             merge_dicts({'X3': ['C']}, {'X1': ['A'], 'X2': ['B']}))
        self.assertDictEqual({'X1': ['A', 'X3'], 'X2': ['B']}, merge_dicts({'X1': ['X3']}, {'X1': ['A'], 'X2': ['B']}))