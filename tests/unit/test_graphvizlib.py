import unittest

from familytreelib import GraphvizLib
from tests.mongo import mongomock_client


class GraphvizLibTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = mongomock_client()

    def test_graphviz_empty_node(self):
        tree = GraphvizLib(0)
        tree.build_tree(self.client.db.braks)
        image_stream = tree.render()
        self.assertIsNotNone(image_stream.read())

    def test_graphviz_build(self):
        tree = GraphvizLib(1)
        tree.build_tree(self.client.db.braks)
        image_stream = tree.render()
        self.assertIsNotNone(image_stream.read())