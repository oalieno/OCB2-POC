#!/usr/bin/env python3
from oracle import Oracle
from block import Block
from color import *

oracle = Oracle('127.0.0.1', 20000)

N = Block.random(16)
M = Block.len(16) + Block.random(16)
T, C = oracle.encrypt(N, M)

T_ = M[2] ^ C[2]
C_ = C[1] ^ Block.len(16)
auth, M_ = oracle.decrypt(N, T_, C_)

if auth == 'True':
    print(f'result = {green("Authenticated")}')
else:
    print(f'result = {red("Not Authenticated")}')
