import unittest
from palindromes.dicttree import DictTree
from palindromes.cursor   import Cursor


class testDictTree(unittest.TestCase):
    def setUp(self):
        d = DictTree()
        d.add_word("beaver")
        d.add_word("bean")
        d.add_word("beach")
        self.d = d
        self.expected_numNodes = 13
    def testNumNodes(self):
        self.assertEqual(self.d.numNodes,self.expected_numNodes)
    def testAdd(self):
        d = self.d
        d.add_word("poop")
        self.assertTrue(d.has_word("poop"))
    def testNotHas_one_less(self):
        d = self.d
        self.assertFalse(d.has_word("beave"))
    def testNotHas_last_off(self):
        d = self.d
        self.assertFalse(d.has_word("beaven"))
    def testAddTwoOverlap1(self):
        d = self.d
        d.add_word("poop")
        d.add_word("poo")  
        self.assertTrue(d.has_word("poo"))
        self.assertTrue(d.has_word("poop"))
    def testAddTwoOverlap2(self):
        d = self.d
        d.add_word("poo")
        d.add_word("poop")  
        self.assertTrue(d.has_word("poo"))
        self.assertTrue(d.has_word("poop"))
    def testSetCursor(self):
        c = Cursor(self.d)
        self.assertTrue(c.move_down("bea"))
    def testChildrenAtCursor(self):
        c = Cursor(self.d)
        self.assertTrue(c.move_down("bea"))
        self.assertEqual(c.get_edge_set(),set(['v','n','c']))
        self.assertTrue(c.move_down("beach"))
        self.assertEqual(c.get_edge_set(),set(['']))

if __name__ == '__main__':
    unittest.main()

