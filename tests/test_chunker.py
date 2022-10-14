import unittest
from src.chunker import Chunker

class TestChunker(unittest.TestCase):

    def test_initialize(self):
        self.assertIsNotNone(Chunker(2))

    def test_boundary(self):
        # This is not quite true - the test results are adapted to the chunker!
        # that's a bit off, but in general do work as a sanity check
        c = Chunker(2)
        self.assertTrue (c.isBoundary(b'\x00'*64))
        self.assertTrue (c.isBoundary(b'\x00'*63 + b'\x01'*1))
        self.assertTrue (c.isBoundary(b'\x00'*16 + b'\xff'*48))
        self.assertTrue (c.isBoundary(b'\x00'*32 + b'\xff'*32))
        self.assertTrue (c.isBoundary(b'\x00'*48 + b'\xff'*16))
        self.assertTrue (c.isBoundary(b'\x00'*2  + b'\xff'*62))
        self.assertTrue (c.isBoundary(b'\x00\xfe' + b'\xff'*62))
        self.assertFalse(c.isBoundary(b'\x00'*1  + b'\xff'*63))
        self.assertFalse(c.isBoundary(b'\xff'*64))

        c = Chunker(32)
        self.assertTrue (c.isBoundary(b'\x00'*64))
        self.assertTrue (c.isBoundary(b'\x00'*63 + b'\x01'*1))
        self.assertTrue (c.isBoundary(b'\x00'*48 + b'\xff'*16))
        self.assertTrue (c.isBoundary(b'\x00'*32 + b'\xff'*32))
        self.assertTrue (c.isBoundary(b'\x00'*31 + b'\xfe' + b'\xff'*32))
        self.assertFalse(c.isBoundary(b'\x00'*31 + b'\xff' + b'\xff'*32))
        self.assertFalse(c.isBoundary(b'\x00'*16 + b'\xff'*48))
        self.assertFalse(c.isBoundary(b'\xff'*64))

        c = Chunker(64)
        self.assertTrue (c.isBoundary(b'\x00'*64))
        self.assertTrue (c.isBoundary(b'\x00'*63 + b'\xfe'*1))
        self.assertFalse(c.isBoundary(b'\x00'*63 + b'\xff'*1))
        self.assertFalse(c.isBoundary(b'\x00'*48 + b'\xff'*16))
        self.assertFalse(c.isBoundary(b'\x00'*32 + b'\xff'*32))
        self.assertFalse(c.isBoundary(b'\x00'*16 + b'\xff'*48))
        self.assertFalse(c.isBoundary(b'\xff'*64))

# TODO generate random byte arrays and check whether the statistics hold
