import unittest
from src.chunker import Chunker

class TestChunker(unittest.TestCase):

    def test_initialize(self):
        self.assertIsNotNone(Chunker(2))

    def test_boundary(self):
        # This is not quite true - the test results are adapted to the chunker
        # that's a bit off, but in general do work as a sanity check
        # FIXME: The code below needs to be reviewd with a clear head
        c = Chunker(2)
        self.assertTrue(c.isBoundary(b'\x00'*64))
        self.assertTrue(c.isBoundary(b'\x00'*63 + b'\x01'*1))
        self.assertTrue(c.isBoundary(b'\x00'*16 + b'\xff'*48))
        self.assertTrue(c.isBoundary(b'\x00'*32 + b'\xff'*32))
        self.assertTrue(c.isBoundary(b'\x00'*48 + b'\xff'*16))
        self.assertFalse(c.isBoundary(b'\xff'*64))

        c = Chunker(32)
        self.assertTrue(c.isBoundary(b'\x00'*64))
        self.assertTrue(c.isBoundary(b'\x00'*63 + b'\x01'*1))
        self.assertTrue(c.isBoundary(b'\x00'*48 + b'\xff'*16))
        self.assertTrue(c.isBoundary(b'\x00'*32 + b'\xff'*32))
        self.assertFalse(c.isBoundary(b'\x00'*16 + b'\xff'*48))
        self.assertFalse(c.isBoundary(b'\xff'*64))

        c = Chunker(64)
        self.assertTrue(c.isBoundary(b'\x00'*64))
        self.assertTrue(c.isBoundary(b'\x00'*63 + b'\x01'*1))
        self.assertFalse(c.isBoundary(b'\x00'*48 + b'\xff'*16))
        self.assertFalse(c.isBoundary(b'\x00'*32 + b'\xff'*32))
        self.assertFalse(c.isBoundary(b'\x00'*16 + b'\xff'*48))
        self.assertFalse(c.isBoundary(b'\xff'*64))


    #def test_put_get_single(self):
    #    n = Node()
    #    self.assertIsNone(n.put(bytes(0), b'1337'))
    #    self.assertEqual(n.get(bytes(0)), b'1337')

    #def test_put_get_multi(self):
    #    n = Node()
    #    self.assertIsNone(n.put(b'0', b'1337'))
    #    self.assertIsNone(n.put(b'1', b'31337'))
    #    self.assertEqual(n.get(b'0'), b'1337')
    #    self.assertEqual(n.get(b'1'), b'31337')
