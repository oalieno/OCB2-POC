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
T, C = oracle.encrypt(N, M)

T_ = M[length + 1] ^ C[length + 1]
C_ = Block()
last = Block.zero()
for i in range(1, length):
    C_ = C_ + C[i]
    last = last ^ M[i]
C_ = C_ + (last ^ C[length] ^ Block.len(16))
auth, M_ = oracle.decrypt(N, T_, C_)

if auth == 'True':
    print(f'result = {green("Authenticated")}')
else:
    print(f'result = {red("Not Authenticated")}')
