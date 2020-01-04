#!/usr/bin/env python3
from oracle import Oracle
from block import *
from color import *
from mapping import *

oracle = Oracle('127.0.0.1', 20000)

def recovery(N, M, C, T):
    L = specificMapping(oracle, [N])[0]

    n = C.blocksize()
    if n == 1:
        Y = specificMapping(oracle, [Block.len(16) ^ L.double()])
        M_ = Y[0] ^ C[0]
    elif n == 2:
        Y = specificMappingInv(oracle, [C[0] ^ L.double()])
        M_ = Y[0] ^ L.double()
        Y = specificMapping(oracle, [Block.len(16) ^ L.double(2)])
        M_ += Y[0] ^ C[1]
    else:
        L_ = L.double() ^ L.double(2)
        C[0], C[1] = C[1] ^ L_, C[0] ^ L_
        auth, M_ = oracle.decrypt(N, C, T)
        M_[0], M_[1] = M_[1] ^ L_, M_[0] ^ L_

    if M == M_:
        print(f'result = {green("Plaintext Recovered")}')
    else:
        print(f'result = {red("Plaintext Not Recovered")}')

N = Block.random(16)
M = Block.random(16 * 3)
C, T = oracle.encrypt(N, M)
print('-' * 10)
print('Plaintext Recovery')
print('-' * 10)
print(f'N = {N.hex()}')
print(f'C = {C.hex()}')
print(f'T = {T.hex()}')
print()
recovery(N, M, C, T)
