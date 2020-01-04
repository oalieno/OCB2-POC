#!/usr/bin/env python3
from oracle import Oracle
from block import Block
from color import *

import sys
if len(sys.argv) < 2:
    print(f'usage : {sys.argv[0]} <forgery message length>')
length = int(sys.argv[1])

oracle = Oracle('127.0.0.1', 20000)

N = Block.random(16)
M = Block.random((length - 1) * 16) + Block.len(16) + Block.random(16)
C, T = oracle.encrypt(N, M)

C_ = Block()
T_ = M[length] ^ C[length]
Z = Block.zero()
for i in range(length - 1):
    C_ += C[i]
    Z ^= M[i]
C_ += (Z ^ C[length - 1] ^ Block.len(16))
auth, M_ = oracle.decrypt(N, C_, T_)

if auth:
    print(f'result = {green("Authenticated")}')
else:
    print(f'result = {red("Not Authenticated")}')
