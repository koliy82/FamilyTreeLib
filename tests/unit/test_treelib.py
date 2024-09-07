import unittest

from familytreelib import TreeLib
from tests.mongo import mongomock_client


class TreeLibTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = mongomock_client()

    def test_treelib_empty_node(self):
        tree = TreeLib(0)
        tree.build_tree(self.client.db.braks)
        formatted_tree = tree.tree.show(stdout=False, reverse=True)
        self.assertEqual(formatted_tree, 'Empty\n')

    def test_treelib_build(self):
        tree = TreeLib(1)
        tree.build_tree(self.client.db.braks)
        formatted_tree = tree.tree.show(stdout=False, reverse=True)
        print("tree:")
        print(formatted_tree)
        self.assertEqual(formatted_tree, 'test 1\n├── test 𝚖𝚘𝚛𝚊ᵃʳ\n└── test 3🌱\n    ├── test 5👈\n    │   ├── test 6🇺🇲\n    │   └── ?\n    │       └── test 8\n    └── ?\n')

    def test_treelib_max_duplicate(self):
        tree = TreeLib(5)
        tree.build_tree(self.client.db.braks)
        formatted_tree = tree.tree.show(stdout=False, reverse=True)
        self.assertEqual(formatted_tree, 'test 5👈\n├── test 6🇺🇲\n└── ?\n    └── test 8\n')

    def test_treelib_max_duplicate_2(self):
        tree = TreeLib(7493530812)
        tree.build_tree(self.client.db.braks)
        formatted_tree = tree.tree.show(stdout=False, reverse=True)
        self.assertEqual(formatted_tree, '?\n├── ?\n└── ?\n    └── ?\n')