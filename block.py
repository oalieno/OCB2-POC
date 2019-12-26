#!/usr/bin/env python3
from os import urandom

class Block:
    def __init__(self, data = b'', blocksize = 16):
        self.data = data
        self.blocksize = blocksize

    @classmethod
    def random(cls, size):
        return cls(urandom(size))

    @classmethod
    def len(cls, n):
        return cls(int(n * 8).to_bytes(16, 'big'))

    @classmethod
    def zero(cls):
        return cls(int(0).to_bytes(16, 'big'))

    def size(self):
        return len(self.data) // self.blocksize

    def hex(self):
        return self.data.hex()

    def __add__(self, other):
        return Block(self.data + other.data)

    def __xor__(self, other):
        return Block(bytes([x ^ y for x, y in zip(self.data, other.data)]))

    def __getitem__(self, key):
        key -= 1 # paper use 1-based index
        return Block(self.data[key * self.blocksize : (key + 1) * self.blocksize])
