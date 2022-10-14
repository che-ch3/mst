import unittest
from src.node import Node, Item
from src.chunker import Chunker
from hashlib import sha512

class TestNodesBasic(unittest.TestCase):

    def test_create_empty(self):
        self.assertIsNotNone(Node())
        self.assertEqual(Node().items, ())
        self.assertEqual(Node().level, 0)

    def test_create_from_pairs(self):
        self.assertIsNotNone(Node(()))
        self.assertEqual(Node().items, ())
        self.assertEqual(Node().level, 0)

        pairs = ((b'0', b'1337'),)
        n = Node(pairs=pairs)
        self.assertIsNotNone(n)
        self.assertTupleEqual(n.to_tuple(), pairs)
        self.assertEqual(n.level, 0)

        pairs = ((b'0', b'1337'), (b'1', b'31337'))
        n = Node(pairs=pairs)
        self.assertIsNotNone(n)
        self.assertTupleEqual(n.to_tuple(), pairs)
        self.assertEqual(n.level, 0)

    def test_create_from_items(self):
        pairs = ((b'0', b'1337'),)
        items = tuple([Item(key, sha512(value).digest()) for key, value in pairs])
        n = Node(items=items)
        self.assertIsNotNone(n)
        self.assertTupleEqual(n.items, items)
        self.assertEqual(n.level, 0)

        pairs = ((b'0', b'1337'), (b'1', b'31337'))
        items = tuple([Item(key, sha512(value).digest()) for key, value in pairs])
        n = Node(items=items)
        self.assertIsNotNone(n)
        self.assertTupleEqual(n.items, items)
        self.assertEqual(n.level, 0)

    def test_create_from_node(self):
        n = Node(pairs=((b'0', b'1337'),))
        m = Node(nodes=((b'0', n),))
        self.assertIsNotNone(n)
        self.assertIsNotNone(m)
        self.assertEqual(n.level, 0)
        self.assertEqual(m.level, 1)
        self.assertEqual(m.get(b'0'), b'1337')

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

    def test_chunking(self):
        pairs=((b'0', b'\xff\xff\xff'),
               (b'1', (714).to_bytes(64, 'big')),
               (b'2', (0).to_bytes(64, 'big')))
        n = Node(pairs=pairs, chunker=Chunker(2))
        self.assertEqual(n.level, 1)
        self.assertTupleEqual(n.to_tuple(), pairs)

    #def test_put_get_multi(self):
    #    # TODO double insert
    #    pass
