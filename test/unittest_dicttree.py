import unittest
from palindromes.dicttree import DictTree

class TestDictTree(unittest.TestCase):
    def setUp(self):
        self.empty_tree = DictTree()
        self.sample_words = ["apple", "app", "banana", "band", "bandana"]
        self.tree = DictTree(self.sample_words.copy())

    def test_init_empty(self):
        # empty tree has only root node and no words
        self.assertEqual(self.empty_tree.numNodes, 1)
        self.assertEqual(self.empty_tree.numWords, 0)
        self.assertFalse(self.empty_tree.has_word("anything"))

    def test_init_with_words_counts(self):
        # initializing with words populates numWords and numNodes > 1
        dt = DictTree(["a", "ab", "abc"])
        self.assertEqual(dt.numWords, 3)
        self.assertGreater(dt.numNodes, 1)
        for w in ["a", "ab", "abc"]:
            self.assertTrue(dt.has_word(w))

    def test_add_word_increases_counts(self):
        initial_nodes = self.empty_tree.numNodes
        initial_words = self.empty_tree.numWords
        self.empty_tree.add_word("cat")
        self.assertEqual(self.empty_tree.numWords, initial_words + 1)
        self.assertTrue(self.empty_tree.has_word("cat"))
        # adding overlapping word reuses nodes
        self.empty_tree.add_word("car")
        self.assertEqual(self.empty_tree.numWords, initial_words + 2)
        self.assertTrue(self.empty_tree.has_word("car"))
        self.assertGreaterEqual(self.empty_tree.numNodes, initial_nodes + 3)

    def test_add_words_bulk(self):
        dt = DictTree()
        dt.add_words(["x", "xy", "xyz"])
        self.assertTrue(dt.has_word("x"))
        self.assertTrue(dt.has_word("xy"))
        self.assertTrue(dt.has_word("xyz"))
        self.assertEqual(dt.numWords, 3)

    def test_has_word_allow_partial(self):
        # without allow_partial, partial matches fail
        self.assertFalse(self.tree.has_word("ban"))
        # with allow_partial, should succeed
        self.assertTrue(self.tree.has_word("ban", allow_partial=True))

    def test_not_has_word(self):
        self.assertFalse(self.tree.has_word("bandit"))
        self.assertFalse(self.tree.has_word(""))

    def test_repeated_add(self):
        dt = DictTree()
        dt.add_word("dup")
        dt.add_word("dup")
        self.assertEqual(dt.numWords, 2)
        self.assertTrue(dt.has_word("dup"))

    def test_long_word(self):
        long_word = "q" * 100
        self.empty_tree.add_word(long_word)
        self.assertTrue(self.empty_tree.has_word(long_word))
        self.assertEqual(self.empty_tree.numWords, 1)

    def test_num_nodes_consistency(self):
        words = ["red", "green", "blue"]
        dt = DictTree(words)
        # build all distinct prefixes (including empty root "")
        prefixes = { w[:i] for w in words for i in range(len(w) + 1) }
        # now assert that numNodes equals number of unique prefixes
        self.assertEqual(dt.numNodes, len(prefixes))

if __name__ == "__main__":
    unittest.main()
