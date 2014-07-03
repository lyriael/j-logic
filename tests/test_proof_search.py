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

    def test_conquer1(self):
        ps = ProofSearch({}, '(((a*b)*(!c)):(c:F))')
        terms_to_match = ps.divide()['(((a*b)*(!c)):(c:F))']
        self.assertListEqual([('a', '(X3->((c:X2)->(c:F)))'), ('b', 'X3'), ('c', 'X2')], terms_to_match)

    def test_get_configurations(self):
        ps = ProofSearch({'a': ['(G->H)', '(A->(G->F))', '((b:B)->(H->F))', '((H->F)->(G->F))']}, '')
        term = ('a', '(X2->(X1->F))')
        self.assertDictEqual({'X1': ['', 'G', 'H', 'G'], 'X2': ['', 'A', '(b:B)', '(H->F)']}, ps.get_configurations(term))