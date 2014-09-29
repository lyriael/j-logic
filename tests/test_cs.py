from cs import CS
import unittest


class Tests(unittest.TestCase):

    def test_find_false(self):
        cs = CS({'a': [1, 2, 3], 'b':[]})
        match = cs.find('b', '')
        self.assertFalse(match[0])
        match = cs.find('c', '')
        self.assertFalse(match[0])

    def test_find_true(self):
        cs = CS({'a': ['asdf', 'sf', 'asdfd'], 'b': ['', 'faX', 'aXsXX']})
        match = cs.find('a', 'sf')
        self.assertTrue(match)
        match = cs.find('a', 'asdf')
        self.assertTrue(match)

    def test_find_list(self):
        cs = CS({'a': ['(A->B)', 'C', '(C->D)', '((A->B)->C)']})
        orig_term = '(X1->X2)'
        match = cs.find('a', orig_term)
        self.assertTrue(match[0])
        self.assertListEqual([{'X2': 'B', 'X1': 'A'}, {'X2': 'D', 'X1': 'C'}, {'X2': 'C', 'X1': '(A->B)'}], match[1])

    def test_find_list1(self):
        cs = CS({'a': ['(A->(A->F))', '((b:B)->A)', 'B', '(C->(A->F))', '((b:B)->(B->F))'], 'b': ['B']})
        orig_term = '(X2->(X1->F))'
        match = cs.find('a', orig_term)
        print(match)
        self.assertTrue(match[0])
        self.assertListEqual([{'X2': 'A', 'X1': 'A'}, {'X2': 'C', 'X1': 'A'}, {'X2': '(b:B)', 'X1': 'B'}], match[1])

    # mixing Y's and wilds
    def test_find_list2(self):
        cs = CS({'a': ['(Y1->(Y2->Y3))', '(Y1->Y2)']})
        orig_term = '(X1->X2)'
        match = cs.find('a', orig_term)
        self.assertTrue(match[0])
        # second fits, but needs no wild
        self.assertListEqual([], match[1])

    # mixing Y's and wilds
    def test_find_list3(self):
        orig_term = '(X2->(X1->F))'
        cs = CS({'a': ['(Y1->(Y2->Y1))'], 'b': ['B']})
        match = cs.find('a', orig_term)
        self.assertTrue(match[0])
        # Y-wilds must be saved, if they determine a X!!!
        self.assertListEqual([{'X2': 'F'}], match[1])





