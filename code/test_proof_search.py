import unittest
from proof_search import *
from helper import configs_to_table


class Tests(unittest.TestCase):

    def test_conquer_one(self):
        ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X2->(X1->F))'), ('b', 'B')]
        one = ps.conquer_one('test')
        self.assertListEqual([(['A', 'A'], []),
                              (['A', 'C'], []),
                              (['B', '(b:B)'], [])],
                             one)

    def test_conquer_one2(self):
        ps = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']}, '')
        ps.atoms = ['test']
        ps.musts['test'] = [('a', '(X2->(X1->F))'), ('b', 'C')]
        one = ps.conquer_one('test')
        self.assertIsNone(one)

    def test_conquer_one3(self):
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

    def test_apply_condition1(self):
        wild = ['A', 'B', '']
        con = ('X1', 'A')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(wild, config)
        self.assertIsNone(condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition2(self):
        wild = ['A', 'B', '']
        con = ('X1', 'B')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertIsNone(config)
        self.assertIsNone(condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition3(self):
        wild = ['A', 'B', '']
        con = ('X3', 'C')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(['A', 'B', 'C'], config)
        self.assertIsNone(condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition4(self):
        wild = ['', 'B', '']
        con = ('X1', 'X3')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(wild, config)
        self.assertEqual(con, condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition5(self):
        wild = ['A', 'B', '']
        con = ('X1', 'X3')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(['A', 'B', 'A'], config)
        self.assertIsNone(condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition6(self):
        wild = ['(A->F)', 'A']
        con = ('X1', '(X2->F)')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(wild, config)
        self.assertIsNone(condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition7(self):
        wild = ['(B->(A->F))', 'A', '']
        con = ('X1', '(X3->(X2->F))')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(['(B->(A->F))', 'A', 'B'], config)
        self.assertIsNone(condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition8(self):
        wild = ['(B->(A->F))', 'A', 'C']
        con = ('X1', '(X3->(X2->F))')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertIsNone(config)
        self.assertIsNone(condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition9(self):
        wild = ['', 'B', 'C']
        con = ('X1', '(X2->X3)')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(['(B->C)', 'B', 'C'], config)
        self.assertIsNone(condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition10(self):
        wild = ['', 'B', '']
        con = ('X1', '(X2->X3)')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(wild, config)
        self.assertEqual(('X1', '(B->X3)'), condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition11(self):
        wild = ['', 'B', '']
        con = ('X1', '(Y2->F)')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(['', 'B', ''], config)
        self.assertEqual(con, condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition12(self):
        wild = ['(B->F)', '', '']
        con = ('X1', '(Y2->F)')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(['(B->F)', '', ''], config)
        self.assertIsNone(condition)
        self.assertDictEqual({'Y2': 'B'}, y_wilds)

    def test_apply_condition13(self):
        wild = ['(B->(A->B))', '', '']
        con = ('X1', '(Y1->Y2)')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(wild, config)
        self.assertIsNone(condition)
        self.assertDictEqual({'Y1': 'B', 'Y2': '(A->B)'}, y_wilds)

    def test_apply_condition14(self):
        wild = ['B', '', '']
        con = ('X1', '(Y2->F)')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertIsNone(config)
        self.assertIsNone(condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition15(self):
        wild = ['', 'B']
        con = ('X1', '(Y2->X2)')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(wild, config)
        self.assertEqual(('X1', '(Y2->B)'), condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition16(self):
        wild = ['(A->B)', '']
        con = ('X1', '(Y2->X2)')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(['(A->B)', 'B'], config)
        self.assertIsNone(condition)
        self.assertEqual({'Y2': 'A'}, y_wilds)

    def test_apply_condition17(self):
        wild = ['(A->B)', 'C']
        con = ('X1', '(Y2->X2)')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertIsNone(config)
        self.assertIsNone(condition)
        self.assertIsNone(y_wilds)

    def test_apply_condition18(self):
        wild = ['(A->B)', 'B']
        con = ('X1', '(Y2->X2)')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertListEqual(['(A->B)', 'B'], config)
        self.assertIsNone(condition)
        self.assertEqual({'Y2': 'A'}, y_wilds)

    def test_apply_condition19(self):
        wild = ['(A->B)', '', 'B']
        con = ('X2', '(X3->Y1)')
        config, condition, y_wilds = apply_condition(wild, con)
        self.assertEqual(wild, config)
        self.assertEqual(('X2', '(B->Y1)'), condition)
        self.assertIsNone(y_wilds)

    def test_merge_two_tables(self):
        t1 = [(['A', 'B', ''], [])]
        t2 = [(['A', '', 'C'], [])]
        self.assertListEqual([(['A', 'B', 'C'], [])], merge_two_tables(t1, t2))

    def test_merge_two_tables2(self):
        t1 = [(['D', 'C', '', 'B', ''], []),
              (['C', 'C', '', 'C', ''], [])]
        t2 = [(['D', '', '', '', 'A'], []),
              (['A', '', '', '', 'D'], [])]
        self.assertListEqual([(['D', 'C', '', 'B', 'A'], [])], merge_two_tables(t1, t2))

    def test_merge_two_tables3(self):
        t1 = [(['', ''], [('X1', '(Y2->X2)')])]
        t2 = [(['', 'C'], [])]
        table = merge_two_tables(t1, t2)
        table2 = merge_two_tables(t2, t1)
        self.assertEqual(table, table2)

    def test_find_all1(self):
        ps = ProofSearch({'a': [1, 2, 3]}, '')
        match = ps.look_up_in_cs('b', '')
        self.assertIsNone(match)

    def test_find_all2(self):
        cs = ProofSearch({'a': ['(A->B)', 'C', '(C->D)', '((A->B)->C)']}, '')
        orig_term = '(X1->X2)'
        match = cs.look_up_in_cs('a', orig_term)
        self.assertListEqual([({'X2': 'B', 'X1': 'A'}, []), ({'X2': 'D', 'X1': 'C'}, []), ({'X2': 'C', 'X1': '(A->B)'}, [])], match)

    def test_find_all3(self):
        cs = ProofSearch({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']}, '')
        orig_term = '(X2->(X1->F))'
        match = cs.look_up_in_cs('a', orig_term)
        self.assertListEqual([({'X2': 'A',      'X1': 'A'}, []),
                              ({'X2': 'C',      'X1': 'A'}, []),
                              ({'X2': '(b:B)',  'X1': 'B'}, [])],
                             match)

    # mixing Y's and wilds
    def test_find_all4(self):
        cs = ProofSearch({'a': ['(Y1->(Y2->Y3))', '(Y1->Y2)']}, '')
        orig_term = '(X1->X2)'
        match = cs.look_up_in_cs('a', orig_term)
        # second fits, but needs no wild
        self.assertListEqual([({}, [('X2', '(Y2->Y3)')])], match)

    # mixing Y's and wilds
    def test_find_all5(self):
        orig_term = '(X2->(X1->F))'
        cs = ProofSearch({'a': ['(Y1->(Y2->Y1))'], 'b': ['B']}, '')
        match = cs.look_up_in_cs('a', orig_term)
        self.assertListEqual([({'X2': 'F'}, [])], match)

    def test_find_all6(self):
        orig_term = '(X1->(X2->X3))'
        cs = ProofSearch({'a': ['(Y1->(Y2->Y3))']}, '')
        match = cs.look_up_in_cs('a', orig_term)
        self.assertListEqual([], match)

    def test_find_all7(self):
        orig_term = '(A->B)'
        cs = ProofSearch({'a': ['(A->B)', '(Y1->Y2)']}, '')
        match = cs.look_up_in_cs('a', orig_term)
        self.assertListEqual([], match)

    def test_find_all8(self):
        orig_term = '(A->B)'
        cs = ProofSearch({'a': ['(Y1->Y1)']}, '')
        match = cs.look_up_in_cs('a', orig_term)
        self.assertIsNone(match)

    def test_find_all9(self):
        orig_term = '(G->(H->G))'
        ps = ProofSearch({'a': ['((c:X3)->X1)']}, '')
        match = ps.look_up_in_cs('a', orig_term)
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

    def test_apply_all_conditions1(self):
        wild = ['(A->B)', 'C', '']
        con = [('X1', '(Y2->X3)'), ('X3', 'B')]
        config, conditions = apply_all_conditions(wild, con)
        self.assertEqual(['(A->B)', 'C', 'B'], config)
        self.assertEqual([], conditions)

    def test_apply_all_conditions2(self):
        wild = ['(A->B)', 'C', '']
        con = [('X1', '(Y2->X3)'), ('X3', 'C')]
        config, conditions = apply_all_conditions(wild, con)
        self.assertIsNone(config)
        self.assertEqual([], conditions)

    def test_apply_all_conditions3(self):
        wild = ['(A->B)', '', 'B']
        con = [('X2', '(X3->Y1)')]
        config, conditions = apply_all_conditions(wild, con)
        self.assertEqual(['(A->B)', '', 'B'], config)
        self.assertEqual([('X2', '(B->Y1)')], conditions)

    def test_full_merge_of_two_configs(self):
        config1 = ['(A->B)', '', '']
        cond1 = [('X1', '(Y2->X3)'), ('X3', 'B')]
        config2 = ['', '', 'B']
        cond2 = [('X2', '(X3->Y1)')]
        config_a, cond_a = full_merge_of_two_configs((config1, cond1), (config2, cond2))
        self.assertEqual(['(A->B)', '', 'B'], config_a)
        self.assertEqual([('X2', '(B->Y1)')], cond_a)
        config_b, cond_b = full_merge_of_two_configs((config2, cond2), (config1, cond1))
        self.assertEqual(['(A->B)', '', 'B'], config_b)
        self.assertEqual([('X2', '(B->Y1)')], cond_b)

    def test_full_merge_of_two_configs2(self):
        config1, cond1 = ['A', ''], [('X2', '(Y3->B)')]
        config2, cond2 = ['A', ''], [('X2', '(A->Y1)')]
        config, cond = full_merge_of_two_configs((config1, cond1), (config2, cond2))
        print(cond)
        print(config)

    def test_mix_y_and_x_wilds(self):
        # matching Y1->(Y2->Y1) to the must of b: X2->X1 results in a condition with mixed x-y-wilds.
        # this was not expected to happen!
        cs = ProofSearch({'a': ['((A->C)->F)'], 'b': ['(Y1->(Y2->Y1))'], 'c': ['C']}, '((a*(b*c)):F)')

        self.assertIn(('a', '(X1->F)'),     cs.musts.get('((a*(b*c)):F)'))
        self.assertIn(('b', '(X2->X1)'),    cs.musts.get('((a*(b*c)):F)'))
        self.assertIn(('c', 'X2'),          cs.musts.get('((a*(b*c)):F)'))

        configs_and_con_a = cs.look_up_in_cs('a', '(X1->F)')
        configs_and_con_b = cs.look_up_in_cs('b', '(X2->X1)')
        configs_and_con_c = cs.look_up_in_cs('c', 'X2')
        self.assertEqual([({'X1': '(A->C)'},    [])],                   configs_and_con_a)
        self.assertEqual([({},                  [('X1', '(Y2->X2)')])], configs_and_con_b)
        self.assertEqual([({'X2': 'C'},         [])],                   configs_and_con_c)

        merge_a_b = merge_two_tables(configs_to_table(configs_and_con_a, 2), configs_to_table(configs_and_con_b, 2))
        merge_b_a = merge_two_tables(configs_to_table(configs_and_con_b, 2), configs_to_table(configs_and_con_a, 2))
        merge_a_c = merge_two_tables(configs_to_table(configs_and_con_a, 2), configs_to_table(configs_and_con_c, 2))
        merge_c_a = merge_two_tables(configs_to_table(configs_and_con_c, 2), configs_to_table(configs_and_con_a, 2))
        merge_b_c = merge_two_tables(configs_to_table(configs_and_con_b, 2), configs_to_table(configs_and_con_c, 2))
        merge_c_b = merge_two_tables(configs_to_table(configs_and_con_c, 2), configs_to_table(configs_and_con_b, 2))
        self.assertEqual([(['(A->C)', 'C'], [])],                   merge_a_b)
        self.assertEqual([(['(A->C)', 'C'], [])],                   merge_a_c)
        self.assertEqual([(['', 'C'],       [('X1', '(Y2->C)')])],  merge_b_c)
        self.assertEqual(merge_a_b, merge_b_a)
        self.assertEqual(merge_a_c, merge_c_a)
        self.assertEqual(merge_b_c, merge_c_b)

        result = cs.conquer()

    def test_all(self):
        ps = ProofSearch({}, '(((!(a+c))+((a+(!a))*(b*(!c)))):(c:F))')
        self.assertEqual(['(c:F)', '((a*(b*(!c))):(c:F))'], ps.atoms)
        self.assertEqual({'(c:F)': [('c', 'F')],
                          '((a*(b*(!c))):(c:F))': [('a', '(X1->(c:F))'), ('b', '((c:X3)->X1)'), ('c', 'X3')]},
                         ps.musts)
        cs = {'a': ['(H->(c:F))', '(H->(G->(c:F)))', '(E->(c:D))', '((c:D)->(c:F))'],
              'b': ['((c:F)->G)', '((c:D)->(a:F))', '(H->(G->H))', '(Y1->(Y2->Y1))'],
              'c': ['(c:F)', 'G', 'D', '(G->F)']}
        ps.set_cs(cs)
        self.assertEqual([({'X1': 'H'}, []), ({'X1': '(c:D)'}, [])], ps.look_up_in_cs('a', '(X1->(c:F))'))
        self.assertEqual([({'X3': 'F', 'X1': 'G'}, []), ({'X3': 'D', 'X1': '(a:F)'}, []),
                          ({}, [('X1', '(Y2->(c:X3))')])],
                         ps.look_up_in_cs('b', '((c:X3)->X1)'))
        self.assertEqual([({'X3': '(c:F)'}, []), ({'X3': 'G'}, []), ({'X3': 'D'}, []), ({'X3': '(G->F)'}, [])],
                         ps.look_up_in_cs('c', 'X3'))


    #todo: what if two Y's with same name but different origin end up in a condition?

    # def test_presentation(self):
    #     formula = '(((((a*b)*(!b))+((!b)+c))+((!b)*d)):(b:F))'
    #     cs = {'a': ['(G->((b:B)->(b:F)))', '(Y1->(Y2->Y1))'], 'b': ['(b:F)', 'G']}
    #     ps = ProofSearch(cs, formula)
    #     for a in ps.atoms:
    #         print('--------')
    #         print('DIVIDE')
    #         print('atom: ' + a)
    #         print('musts: ' + str(ps.musts[a]))
    #         print('CONQUER')
    #         print('config tables:')
    #         for m in ps.musts[a]:
    #             print(str(m) + ': ' + str(ps._find_all_for(m[0], m[1])))
    #         print('merged:' + str(ps._conquer_one(a)))