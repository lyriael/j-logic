import unittest
from formula import Formula
from tree_node import Node


class Tests(unittest.TestCase):

    def test_make_tree1(self):
        tree = Node.make_tree('(!(a+b))')
        self.assertEqual('(!(a+b))', str(tree))
        self.assertEqual('!', tree.token())

    def test_make_tree2(self):
        tree = Node.make_tree('((!a)+b)')
        self.assertTrue(tree.is_root())
        self.assertEqual('+', tree.root().token())
        self.assertEqual(tree, tree.root())
        self.assertEqual('!', tree.left().token())
        self.assertIsNone(tree.left().left())
        self.assertEqual('a', tree.left().right().token())
        self.assertIsNone(tree.left().right().left())
        self.assertIsNone(tree.left().right().right())
        self.assertEqual('b', tree.right().token())
        self.assertTrue(tree.right().is_leaf())

    def test_find1(self):
        node = Node.make_tree('((!a)+b)')
        self.assertEqual('((!a)+b)', str(node))
        left = node.left()
        self.assertEqual('!', left.token())
        self.assertTrue(node.find())

    def test_find2(self):
        tree = Node.make_tree('!')
        self.assertTrue(tree.find())

    def test_find3(self):
        tree = Node.make_tree('(!a)')
        self.assertTrue(tree.find())

    def test_find4(self):
        tree = Node.make_tree('((!a)+b)')
        self.assertEqual('((!a)+b)', str(tree))
        self.assertTrue(tree.find())
        self.assertTrue(tree.left().find())
        self.assertFalse(tree.right().find())

    def test_find5(self):
        tree = Node.make_tree('((A+(!a))*B)')
        self.assertEqual('((A+(!a))*B)', str(tree))
        self.assertTrue(tree.find())
        self.assertTrue(tree.left().find())
        self.assertTrue(tree.left().right().find())
        self.assertFalse(tree.left().left().find())
        self.assertFalse(tree.right().find())

    def test_find6(self):
        tree = Node.make_tree('((((!(a+b))+(d*e))*(!((f+g)*h))):F)')
        self.assertEqual('((((!(a+b))+(d*e))*(!((f+g)*h))):F)', str(tree))
        self.assertTrue(tree.find())
        self.assertTrue(tree.left().left().find())

    def test_tidy_up_ll(self):
        tree = Node.make_tree('(((!a)+A)*B)')
        self.assertEqual('*', tree.token())
        self.assertEqual('B', tree.right().token())
        self.assertTrue(tree.right().is_leaf())
        self.assertEqual('+', tree.left().token())
        self.assertEqual(6, len(tree))
        self.assertEqual('(((!a)+A)*B)', str(tree))
        bang = tree.left().left()
        self.assertEqual('!', bang.token())
        bang.tidy_up()
        self.assertEqual(3, len(tree))

    def test_tidy_up_rl(self):
        tree = Node.make_tree('(B*((!a)+A))')
        self.assertEqual('(B*((!a)+A))', str(tree))
        self.assertEqual(6, len(tree))
        bang = tree.right().left()
        self.assertEqual('!', bang.token())
        bang.tidy_up()
        self.assertEqual(3, len(tree))

    def test_tidy_up_rr(self):
        tree = Node.make_tree('(B*(A+(!a)))')
        self.assertEqual('(B*(A+(!a)))', str(tree))
        self.assertEqual(6, len(tree))
        bang = tree.right().right()
        self.assertEqual('!', bang.token())
        bang.tidy_up()
        self.assertEqual(3, len(tree))

    def test_tidy_up_lr(self):
        tree = Node.make_tree('((A+(!a))*B)')
        self.assertEqual('((A+(!a))*B)', str(tree))
        self.assertEqual(6, len(tree))
        bang = tree.left().right()
        self.assertEqual('!', bang.token())
        bang.tidy_up()
        self.assertEqual(3, len(tree))

    # def test_tidy_up5(self):
    #     tree = Node.make_tree('((A*(!a))*B)')
    #     self.assertEqual('((A*(!a))*B)', str(tree))
    #     bang = tree.left().right()
    #     print(tree)
    #     bang.tidy_up()
    #     print(tree)
    #     self.assertEqual(1, len(tree))

    def test_replace1(self):
        tree = Node.make_tree('((a+b)+c)')
        node = Node.make_tree('(c+d)')
        tree._replace(tree.right(), node)
        self.assertEqual('((a+b)+(c+d))', str(tree))

    def test_remove_node1(self):
        tree = Node.make_tree('a')
        tree.remove(tree.root())
        self.assertEqual('', str(tree))

    def test_remove_node2(self):
        tree = Node.make_tree('(a*b)')
        tree.remove(tree.left())
        self.assertEqual('', str(tree))

    def test_remove_node3(self):
        tree = Node.make_tree('(((!a)+b)*c)')
        tree.remove(tree.left().left())
        self.assertEqual('(b*c)', str(tree))

    def test_remove4(self):
        tree = Node.make_tree('((a*b)*c)')
        tree.remove(tree.left().left())
        self.assertEqual('', str(tree))

    def test_remove5(self):
        tree = Node.make_tree('(((a*b)+c)*d)')
        tree.remove(tree.left().left())
        self.assertEqual('(c*d)', str(tree))

    def test_remove_bangs(self):
        tree = Node.make_tree('((!a)*b)')
        tree.remove_bangs(tree.root())
        self.assertEqual('', str(tree))

    def test_remove_bangs2(self):
        tree = Node.make_tree('(((!a)+c)*b)')
        tree.remove_bangs(tree.root())
        self.assertEqual('(c*b)', str(tree))

    def test_remove_bangs3(self):
        tree = Node.make_tree('((a+((!b)*c))*d)')
        tree.remove_bangs(tree.root())
        self.assertEqual('(a*d)', str(tree))

    def test_remove_bangs4(self):
        tree = Node.make_tree('((a+(b*(!c)))*d)')
        tree.remove_bangs(tree.root())
        self.assertEqual('((a+(b*(!c)))*d)', str(tree))

    def test_remove_bangs5(self):
        tree = Node.make_tree('(a*((!b)*c))')
        tree.remove_bangs(tree.root())
        self.assertEqual('', str(tree))

    def test_collect_nodes1(self):
        f = Node.make_tree('((a+b)*c)')
        self.assertEqual(1, len(f.collect_nodes(f)))
        self.assertEqual('(a+b)', str(f.collect_nodes(f)[0]))
        self.assertTrue(f.collect_nodes(f)[0].has_parent())
        self.assertEqual('((a+b)*c)', str(f.collect_nodes(f)[0].parent()))

    def test_collect_nodes2(self):
        f = Node.make_tree('((((a+b)*(e+f))+(!c))*d)')
        col = f.collect_nodes(f)
        self.assertEqual(4, len(col))
        for node in col:
            print(str(node))