import unittest

from familytreelib import TreeLib
from tests.mongo import mongomock_client


class TreeLibTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = mongomock_client()
        print("setUpClass")

    def test_treelib_empty_node(self):
        tree = TreeLib(0)
        tree.build_tree(self.client.db.braks)
        formatted_tree = tree.tree.show(stdout=False, reverse=True)
        self.assertEqual(formatted_tree, 'Empty\n')

    def test_treelib_build(self):
        tree = TreeLib(1)
        tree.build_tree(self.client.db.braks)
        formatted_tree = tree.tree.show(stdout=False, reverse=True)
        self.assertEqual(formatted_tree, 'test 1\n├── test 3\n│   └── test 4\n└── test 2\n')


if __name__ == '__main__':
    unittest.main()
