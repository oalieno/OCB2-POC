#!/usr/bin/env python3
from oracle import Oracle
from block import Block
from color import *

oracle = Oracle('127.0.0.1', 20000)

N = Block.random(16)
M = Block.len(16) + Block.random(16)
C, T = oracle.encrypt(N, M)

C_ = C[0] ^ Block.len(16)
T_ = M[1] ^ C[1]
auth, M_ = oracle.decrypt(N, C_, T_)

if auth:
    print(f'result = {green("Authenticated")}')
else:
    print(f'result = {red("Not Authenticated")}')
