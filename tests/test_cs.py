from cs import CS
import unittest


class Tests(unittest.TestCase):

    def test_find_all_for_none(self):
        cs = CS({'a': [1, 2, 3]})
        match = cs.find_all_for('b', '')
        self.assertIsNone(match)

    def test_find_all_for_list(self):
        cs = CS({'a': ['(A->B)', 'C', '(C->D)', '((A->B)->C)']})
        orig_term = '(X1->X2)'
        match = cs.find_all_for('a', orig_term)
        self.assertListEqual([({'X2': 'B', 'X1': 'A'}, []), ({'X2': 'D', 'X1': 'C'}, []), ({'X2': 'C', 'X1': '(A->B)'}, [])], match)

    def test_find_all_for_list1(self):
        cs = CS({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']})
        orig_term = '(X2->(X1->F))'
        match = cs.find_all_for('a', orig_term)
        self.assertListEqual([({'X2': 'A',      'X1': 'A'}, []),
                              ({'X2': 'C',      'X1': 'A'}, []),
                              ({'X2': '(b:B)',  'X1': 'B'}, [])],
                             match)

    # mixing Y's and wilds
    def test_find_all_for_list2(self):
        cs = CS({'a': ['(Y1->(Y2->Y3))', '(Y1->Y2)']})
        orig_term = '(X1->X2)'
        match = cs.find_all_for('a', orig_term)
        # second fits, but needs no wild
        self.assertListEqual([({}, [('X2', '(Y2->Y3)')])], match)

    # mixing Y's and wilds
    def test_find_list3(self):
        orig_term = '(X2->(X1->F))'
        cs = CS({'a': ['(Y1->(Y2->Y1))'], 'b': ['B']})
        match = cs.find_all_for('a', orig_term)
        self.assertListEqual([({'X2': 'F'}, [])], match)

    def test_find_all_for_exact(self):
        orig_term = '(X1->(X2->X3))'
        cs = CS({'a': ['(Y1->(Y2->Y3))']})
        match = cs.find_all_for('a', orig_term)
        self.assertListEqual([], match)

    def test_find_all_for_exact2(self):
        orig_term = '(A->B)'
        cs = CS({'a': ['(A->B)', '(Y1->Y2)']})
        match = cs.find_all_for('a', orig_term)
        self.assertListEqual([], match)

    def test_find_all_for_exact3(self):
        orig_term = '(A->B)'
        cs = CS({'a': ['(Y1->Y1)']})
        match = cs.find_all_for('a', orig_term)
        self.assertIsNone(match)



