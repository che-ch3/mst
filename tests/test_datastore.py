import unittest
from src.datastore import Datastore
from src.node import Node
from hashlib import sha512

class TestDatastore(unittest.TestCase):

    def test_create_empty(self):
        self.assertIsNotNone(Datastore)
        self.assertEqual(Datastore().store, {})

    def test_get_empty(self):
        self.assertFalse(Datastore().get(b''))

    def test_put_get(self):
        ds = Datastore()
        digest = sha512(b'').digest()
        self.assertEqual(ds.put(b''), digest)
        self.assertIsInstance(ds.put(b''), type(b''))
        self.assertEqual(ds.get(ds.put(b'')), b'')

    def test_put_get_node(self):
        ds = Datastore()
        n = Node()

        self.assertFalse(ds.get_node(b'0'*64))

        self.assertTupleEqual(ds.get_node(ds.put_node(n)).to_tuple(), n.to_tuple())
        n.put(b'0', b'1337')
        self.assertTupleEqual(ds.get_node(ds.put_node(n)).to_tuple(), n.to_tuple())
        n.put(b'1', b'31337')
        self.assertTupleEqual(ds.get_node(ds.put_node(n)).to_tuple(), n.to_tuple())
