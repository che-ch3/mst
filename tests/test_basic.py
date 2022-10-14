import unittest
from src.node import Node, Item

class TestNodesBasic(unittest.TestCase):

    def test_create_empty(self):
        self.assertIsNotNone(Node())
        self.assertEqual(Node().items, ())
        self.assertEqual(Node().level, 0)

    def test_get_empty(self):
        self.assertFalse(Node().get(0))

    def test_put_get_single(self):
        n = Node()
        self.assertIsNone(n.put(bytes(0), b'1337'))
        self.assertEqual(n.get(bytes(0)), b'1337')

    def test_put_get_multi(self):
        n = Node()
        self.assertEqual(len(n.items), 0)
        self.assertIsNone(n.put(b'0', b'1337'))
        self.assertEqual(len(n.items), 1)
        self.assertIsNone(n.put(b'1', b'31337'))
        self.assertEqual(len(n.items), 2)
        self.assertEqual(n.get(b'0'), b'1337')
        self.assertEqual(len(n.items), 2)
        self.assertEqual(n.get(b'1'), b'31337')
