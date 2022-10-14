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
        self.assertTupleEqual(n.to_tuple(), ((b'0', b'1337'), (b'1', b'31337')))

        n = Node()
        self.assertEqual(len(n.items), 0)
        self.assertIsNone(n.put(b'1', b'31337'))
        self.assertEqual(len(n.items), 1)
        self.assertIsNone(n.put(b'0', b'1337'))
        self.assertEqual(len(n.items), 2)
        self.assertEqual(n.get(b'0'), b'1337')
        self.assertEqual(len(n.items), 2)
        self.assertEqual(n.get(b'1'), b'31337')
        self.assertTupleEqual(n.to_tuple(), ((b'0', b'1337'), (b'1', b'31337')))

        n = Node()
        self.assertEqual(len(n.items), 0)
        self.assertIsNone(n.put(b'1', b'31337'))
        self.assertEqual(len(n.items), 1)
        self.assertIsNone(n.put(b'0', b'1337'))
        self.assertEqual(len(n.items), 2)
        self.assertIsNone(n.put(b'4', b'13337'))
        self.assertEqual(len(n.items), 3)
        self.assertIsNone(n.put(b'100', b'100'))
        self.assertEqual(len(n.items), 4)
        self.assertEqual(n.get(b'100'), b'100')
        self.assertEqual(len(n.items), 4)
        self.assertEqual(n.get(b'1'), b'31337')
        self.assertEqual(n.get(b'4'), b'13337')
        self.assertEqual(n.get(b'0'), b'1337')
        self.assertEqual(n.get(b'4'), b'13337')
        self.assertEqual(n.get(b'1'), b'31337')
        self.assertEqual(n.get(b'100'), b'100')
        self.assertTupleEqual(n.to_tuple(), ((b'0', b'1337'), (b'1', b'31337'), (b'100', b'100'), (b'4', b'13337')))
    def test_put_rem(self):
        n = Node()
        self.assertEqual(len(n.items), 0)
        n.put(b'1', b'31337')
        self.assertEqual(len(n.items), 1)
        n.remove(b'1')
        self.assertEqual(len(n.items), 0)
        self.assertTupleEqual(n.to_tuple(), ())

    def test_put_rem_multi(self):
        n = Node()
        n.put(b'1', b'31337')
        n.put(b'0', b'1337')
        n.remove(b'1')
        self.assertTupleEqual(n.to_tuple(), ((b'0', b'1337'),))
        n.remove(b'0')
        self.assertTupleEqual(n.to_tuple(), ())

        n.put(b'1', b'31337')
        n.put(b'0', b'1337')
        n.remove(b'0')
        self.assertTupleEqual(n.to_tuple(), ((b'1', b'31337'),))
        n.remove(b'1')
        self.assertTupleEqual(n.to_tuple(), ())

    #def test_put_get_multi(self):
    #    # TODO double insert
    #    pass
