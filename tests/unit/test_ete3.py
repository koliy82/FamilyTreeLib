import unittest

from familytreelib.tree.ete3_model import Ete3Lib
from tests.mongo import mongomock_client


class Ete3LibTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = mongomock_client()

    def test_ete3_empty_node(self):
        tree = Ete3Lib(0)
        tree.build_tree(self.client.db.braks)
        image_stream = tree.render()
        self.assertIsNotNone(image_stream.read())

    def test_ete3_build(self):
        tree = Ete3Lib(1)
        tree.build_tree(self.client.db.braks)
        image_stream = tree.render()
        self.assertIsNotNone(image_stream.read())