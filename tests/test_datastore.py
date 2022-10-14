import unittest
from src.datastore import Datastore
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
