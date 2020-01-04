#!/usr/bin/env python3
from oracle import Oracle
from block import *
from color import *
from mapping import *

oracle = Oracle('127.0.0.1', 20000)

def forgery(N, M):
    N, L = randomMapping(oracle, 1)[0]

    n = M.blocksize()
    X = []
    S = Block.zero()
    for i in range(n - 1):
        X.append(M[i] ^ L.double(i + 1))
        S ^= M[i]
    X.append(Block.len(M[n - 1].size()) ^ L.double(n))

    Y = specificMapping(oracle, X)
    
    C = Block()
    for i in range(n - 1):
        C += Y[i] ^ L.double(i + 1)
    C += Y[n - 1].msb(M[n - 1].size()) ^ M[n - 1]
    
    S ^= Y[n - 1] ^ (C[n - 1] + Block.zero(BLOCKSIZE - C[n - 1].size())) ^ L.double(n + 1) ^ L.double(n)
    T = specificMapping(oracle, [S])[0]

    auth, M_ = oracle.decrypt(N, C, T)

    if auth:
        print(f'result = {green("Authenticated")}')
    else:
        print(f'result = {red("Not Authenticated")}')

N = Block.random(16)
M = Block.random(16)
print('-' * 10)
print('Universal Forgery')
print('-' * 10)
print(f'N = {N.hex()}')
print(f'M = {M.hex()}')
print()
forgery(N, M)
