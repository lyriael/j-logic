import unittest
from proof_search import ProofSearch


class Tests(unittest.TestCase):

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
    #
    # def test_get_configuration2(self):
    #     ps = ProofSearch({'c': ['(A->F)', '(A->T)', '(B->T)', '(C->F)']}, '')
    #     term = ('c', '(X1->F)')
    #     self.assertListEqual([['A', ''], ['C', '']],
    #                          ps.get_configuration(term, 2)[1])
    #
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
    # def test_all_1(self):
    #     ps = ProofSearch({}, '((c*(a*b)):F)')
    #     term, musts = ps.divide().popitem()
    #     self.assertEqual('((c*(a*b)):F)',
    #                      term)
    #     self.assertListEqual([('a', '(X2->X1)'),
    #                           ('b', 'X2'),
    #                           ('c', '(X1->F)')],
    #                          musts)
    #     #cs1 - giving one solution
    #     ps._cs = {'a': ['(S->T)'], 'b': ['S'], 'c': ['(T->F)']}
    #     table = ps.configuration_table(musts)
    #     merge = ps.configuration_merge(table)
    #
    #     self.assertListEqual([('a', [['T',  'S']]),
    #                           ('b', [['',   'S']]),
    #                           ('c', [['T',  '']])],
    #                          table)
    #     self.assertListEqual([['T', 'S']],
    #                          merge)
    #     #cs2 - giving two solutions
    #     ps._cs = {'a': ['(C->T)', '(A->C)', '(A->A)', 'A'],
    #               'b': ['A', 'B', 'C', 'T'],
    #               'c': ['(A->F)', '(A->T)', '(B->T)', '(C->F)']}
    #     table = ps.configuration_table(musts)
    #     merge = ps.configuration_merge(table)
    #     self.assertListEqual([('c', [['A', ''], ['C', '']]),
    #                           ('a', [['T', 'C'], ['C', 'A'], ['A', 'A']]),
    #                           ('b', [['', 'A'], ['', 'B'], ['', 'C'], ['', 'T']])],
    #                          table)
    #     self.assertListEqual([['C', 'A'], ['A', 'A']],
    #                          merge)
    #
    #     #cs3 - giving no sulution
    #     ps._cs = {'a': ['(C->A)', '(B->A)', '(A->B)'],
    #               'b': ['A', '(A->C)'],
    #               'c': ['(A->F)', '(A->T)', '(C->F)']}
    #     table = ps.configuration_table(musts)
    #     merge = ps.configuration_merge(table)
    #     self.assertListEqual([('b', [['', 'A'], ['', '(A->C)']]),
    #                           ('c', [['A', ''], ['C', '']]),
    #                           ('a', [['A', 'C'], ['A', 'B'], ['B', 'A']])], table)
    #     self.assertListEqual([],
    #                            merge)

    def test_all_2(self):
        #TEST 3
        formula = '((((((!a)*b)+(c*d))*((!e)+(f+g)))*(h*i)):F)'
        cs = {}
        ps = ProofSearch(cs, formula)

        #divide
        # parts = ps._formula.to_pieces()
        # for f in parts:
        #     print(f.formula)

        # depends only on 'formula' and not on 'cs'
        splits = ps.divide()
        self.assertDictEqual({'((((c*d)*f)*(h*i)):F)':
                                  [('c', '(X4->(X3->(X1->F)))'), ('d', 'X4'), ('f', 'X3'), ('h', '(X2->X1)'), ('i', 'X2')],
                              '((((c*d)*(!e))*(h*i)):F)':
                                  [('c', '(X5->((e:X4)->(X1->F)))'), ('d', 'X5'), ('e', 'X4'), ('h', '(X2->X1)'), ('i', 'X2')],
                              '((((c*d)*g)*(h*i)):F)':
                                  [('c', '(X4->(X3->(X1->F)))'), ('d', 'X4'), ('g', 'X3'), ('h', '(X2->X1)'), ('i', 'X2')]},
                             splits)

        # TEST 3.2 (compare with cs)
        ps._cs = {  'c': ['(A->((e:B)->(C->F)))', '(A->(B->(C->F)))'],
                    'h': ['(A->(B->F))', '(B->(A->F))', '(B->A)'],
                    'd': ['A'],
                    'a': ['A']} #this should not matter at all, since 'a' is not needed in 'musts'
        term, musts = splits.popitem()
        # print(term)
        # print(musts)
        config = ps.configuration_table(musts)
        # print(config)
        self.assertListEqual([('d', [['', '', '', 'A']]),
                              ('f', [[]]),
                              ('i', [[]]),
                              ('c', [['C', '', '(e:B)', 'A'],
                                     ['C', '', 'B', 'A']]),
                              ('h', [['(B->F)', 'A', '', ''],
                                     ['(A->F)', 'B', '', ''],
                                     ['A', 'B', '', '']])],
                             config)
        merge = ps.configuration_merge(config)
        # print(merge)
        self.assertListEqual([[], [], [], [], [], []], merge)


