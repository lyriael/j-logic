import unittest
from proof_search import ProofSearch


class Tests(unittest.TestCase):

    def test_divide1(self):
        ps = ProofSearch({}, '(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)')
        self.assertDictEqual({'((e*f):F)': [('e', '(X1->F)'), ('f', 'X1')],
                              '((e*g):F)': [('e', '(X1->F)'), ('g', 'X1')]},
                             ps.divide())

    def test_divide2(self):
        ps = ProofSearch({}, '(((!(a*b))+(c*((!d)+e))):((a*b):F))')
        self.assertDictEqual({'((c*e):((a*b):F))': [('c', '(X1->((a*b):F))'), ('e', 'X1')],
                              '((c*(!d)):((a*b):F))': [('c', '((d:X2)->((a*b):F))'), ('d', 'X2')],
                              '((a*b):F)': [('a', '(X1->F)'), ('b', 'X1')]},
                             ps.divide())

    def test_divide3(self):
        ps = ProofSearch({}, '(((a*b)*(!c)):(c:F))')
        terms_to_match = ps.divide()['(((a*b)*(!c)):(c:F))']
        self.assertListEqual([('a', '(X3->((c:X2)->(c:F)))'), ('b', 'X3'), ('c', 'X2')], terms_to_match)

    def test_divide4(self):
        ps = ProofSearch({}, '((((((!a)*b)+(c*d))*((!e)+(f+g)))*(h*i)):F)')
        self.assertDictEqual({'((((c*d)*f)*(h*i)):F)': [('c', '(X4->(X3->(X1->F)))'), ('d', 'X4'), ('f', 'X3'),
                                                        ('h', '(X2->X1)'), ('i', 'X2')],
                              '((((c*d)*(!e))*(h*i)):F)': [('c', '(X5->((e:X4)->(X1->F)))'), ('d', 'X5'), ('e', 'X4'),
                                                           ('h', '(X2->X1)'), ('i', 'X2')],
                              '((((c*d)*g)*(h*i)):F)': [('c', '(X4->(X3->(X1->F)))'), ('d', 'X4'), ('g', 'X3'),
                                                        ('h', '(X2->X1)'), ('i', 'X2')]},
                             ps.divide())

    def test__conquer_one(self):
        ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']}, '')
        term = [('a', '(X2->(X1->F))'), ('b', 'B')]
        one = ps._conquer_one(2, term)
        self.assertListEqual([(['A', 'A'], []),
                              (['A', 'C'], []),
                              (['B', '(b:B)'], [])],
                             one)

    def test__conquer_one1(self):
        ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']}, '')
        term = [('a', '(X2->(X1->F))'), ('b', 'C')]
        one = ps._conquer_one(2, term)
        self.assertIsNone(one)

    def test_conquer(self):
        cs = {'s': ['(B->A)'],
              't': ['B'],
              'v': ['(A->F)']}
        formula = '((v*((s*t)+(!u))):F)'
        ps = ProofSearch(cs, formula)
        self.assertDictEqual({'((v*(s*t)):F)':  [('s', '(X2->X1)'), ('t', 'X2'), ('v', '(X1->F)')],
                              '((v*(!u)):F)':   [('u', 'X2'), ('v', '((u:X2)->F)')]},
                             ps.divide())
        # so sollte das erste aus must erfüllbar sein, aber nicht das zweite.
        self.assertTrue(ps.conquer())
        self.assertTrue(ps._conquer_one(2, [('s', '(X2->X1)'), ('t', 'X2'), ('v', '(X1->F)')])) # '((v*(s*t)):F)'
        self.assertFalse(ps._conquer_one(2, [('u', 'X2'), ('v', '((u:X2)->F)')]))
