from cs import CS
import unittest

class Tests(unittest.TestCase):

    def test_find_false(self):
        cs = CS({'a': [1, 2, 3], 'b':[]})
        match = cs.find('b', '')
        self.assertFalse(match)
        match = cs.find('c', '')
        self.assertFalse(match)

    def test_find_true(self):
        cs = CS({'a': ['asdf', 'sf', 'asdfd'], 'b': ['', 'faX', 'aXsXX']})
        match = cs.find('a', 'sf')
        self.assertTrue(match)
        match = cs.find('a', 'asdf')
        self.assertTrue(match)
