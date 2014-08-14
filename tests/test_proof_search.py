import unittest
from proof_search import ProofSearch


class Tests(unittest.TestCase):
    #
    # def test_divide1(self):
    #     ps = ProofSearch({}, '(((!(((!a)+b)*(c*(!d))))+(e*(f+g))):F)')
    #     self.assertDictEqual({'((e*f):F)': [('e', '(X1->F)'), ('f', 'X1')],
    #                           '((e*g):F)': [('e', '(X1->F)'), ('g', 'X1')]},
    #                          ps.divide())
    #
    # def test_divide2(self):
    #     ps = ProofSearch({}, '(((!(a*b))+(c*((!d)+e))):((a*b):F))')
    #     self.assertDictEqual({'((c*e):((a*b):F))': [('c', '(X1->((a*b):F))'), ('e', 'X1')],
    #                           '((c*(!d)):((a*b):F))': [('c', '((d:X2)->((a*b):F))'), ('d', 'X2')],
    #                           '((a*b):F)': [('a', '(X1->F)'), ('b', 'X1')]},
    #                          ps.divide())
    #
    # def test_divide3(self):
    #     ps = ProofSearch({}, '(((a*b)*(!c)):(c:F))')
    #     terms_to_match = ps.divide()['(((a*b)*(!c)):(c:F))']
    #     self.assertListEqual([('a', '(X3->((c:X2)->(c:F)))'), ('b', 'X3'), ('c', 'X2')], terms_to_match)
    #
    # def test_get_configuration(self):
    #     ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))']}, '')
    #     term = ('a', '(X2->(X1->F))')
    #     self.assertListEqual([['A', 'A', '', '', '', ''], ['A', 'C', '', '', '', ''], ['B', '(b:B)', '', '', '', '']],
    #                          ps.get_configuration(term, 6)[1])

    def test_get_configuration2(self):
        ps = ProofSearch({'a': ['(C->T)', '(A->C)', '(A->T)', 'A'],
                  'b': ['A', 'B', 'C', 'T'],
                  'c': ['(A->F)', '(A->T)', '(B->T)', '(C->F)']}, '')
        term = ('c', '(X1->F)')
        self.assertListEqual([['A', ''], ['C', '']],
                             ps.get_configuration(term, 2)[1])
        print(ps.get_configuration(term, 2)[1])
        print('================================')

    # def test_configuration_to_table(self):
    #     ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'],
    #                       'b': ['A', 'B', '(b:B)', '(A->A)', '(C->B)'],
    #                       'c': ['(B->B)', '(A->A)', '(A->B)']}, '')
    #     m = [('a', '(X2->(X1->F))'), ('a', '((b:X5)->X2)'),
    #          ('a', 'X6'), ('b', 'X5'), ('b', '(X3->X1)'), ('c', '(X6->X1)')]
    #     self.assertListEqual([('a',
    #                            [['', 'A', '', '', 'B', ''],
    #                             ['', '(B->F)', '', '', 'B', '']]),
    #                           ('b',
    #                            [['A', '', 'A', '', '', ''],
    #                             ['B', '', 'C', '', '', '']]),
    #                           ('a',
    #                            [['A', 'A', '', '', '', ''],
    #                             ['A', 'C', '', '', '', ''],
    #                             ['B', '(b:B)', '', '', '', '']]),
    #                           ('c',
    #                            [['B', '', '', '', '', 'B'],
    #                             ['A', '', '', '', '', 'A'],
    #                             ['B', '', '', '', '', 'A']]),
    #                           ('a',
    #                            [['', '', '', '', '', '(A->(A->F))'],
    #                             ['', '', '', '', '', '((b:B)->A)'],
    #                             ['', '', '', '', '', 'B'],
    #                             ['', '', '', '', '', '(C->(A->F))'],
    #                             ['', '', '', '', '', '((b:B)->(B->F))']]),
    #                           ('b',
    #                            [['', '', '', '', 'A', ''],
    #                             ['', '', '', '', 'B', ''],
    #                             ['', '', '', '', '(b:B)', ''],
    #                             ['', '', '', '', '(A->A)', ''],
    #                             ['', '', '', '', '(C->B)', '']])]
    #                          , ps.configuration_table(m))
    #
    # def test_1_all(self):
    #     ps = ProofSearch({}, '((c*(a*b)):F)')
    #     term, musts = ps.divide().popitem()
    #     self.assertEqual('((c*(a*b)):F)',
    #                      term)
    #     self.assertListEqual([('a', '(X2->X1)'),
    #                           ('b', 'X2'),
    #                           ('c', '(X1->F)')],
    #                          musts)
    #     # #cs1
    #     # ps._cs = {'a': ['(S->T)'], 'b': ['S'], 'c': ['(T->F)']}
    #     # table = ps.configuration_table(musts)
    #     # merge = ps.configuration_merge(table)
    #     #
    #     # self.assertListEqual([('a', [['T',  'S']]),
    #     #                       ('b', [['',   'S']]),
    #     #                       ('c', [['T',  '']])],
    #     #                      table)
    #     # self.assertListEqual([['T', 'S']],
    #     #                      merge)
    #     #cs2
    #     ps._cs = {'a': ['(C->T)', '(A->C)', '(A->T)', 'A'],
    #               'b': ['A', 'B', 'C', 'T'],
    #               'c': ['(A->F)', '(A->T)', '(B->T)', '(C->F)']}
    #     table = ps.configuration_table(musts)
    #     print(table)
    #     merge = ps.configuration_merge(table)
    #     self.assertListEqual([('a', [['T', 'C'], ['C', 'A'], ['T', 'A']]),
    #                           ('b', [['', 'A'], ['', 'B'], ['', 'C'], ['', 'T']]),
    #                           ('c', [['A', ''], ['A', ''], ['B', ''], ['C', '']])],
    #                          table)
    #     # self.assertListEqual([], merge)
