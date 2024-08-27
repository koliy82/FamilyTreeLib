import unittest

from familytreelib import IgraphLib
from tests.mongo import mongomock_client


class IgraphLibTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = mongomock_client()

    def test_igraph_empty_node(self):
        tree = IgraphLib(0)
        tree.build_tree(self.client.db.braks)
        image_stream = tree.render()
        self.assertIsNotNone(image_stream.read())

    def test_igraph_build(self):
        tree = IgraphLib(1)
        tree.build_tree(self.client.db.braks)
        image_stream = tree.render()
        self.assertIsNotNone(image_stream.read())