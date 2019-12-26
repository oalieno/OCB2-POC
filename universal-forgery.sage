#!/usr/bin/env python3
from oracle import Oracle
from block import Block
from color import *

oracle = Oracle('127.0.0.1', 20000)

G.<x> = GF(2 ** 128, modulus = 1 + x + x ^ 2 + x ^ 7 + x ^ 128)

def b2f(x):
    assert(len(x.data) == 16)
    return G(Integer(int.from_bytes(x.data, 'big')).bits())

def f2b(x):
    return Block(int(x.integer_representation()).to_bytes(16, 'big'))

def randomMapping(length):
    length += 1

    N = Block.random(16)
    M = Block.random((length - 1) * 16) + Block.len(16) + Block.random(16)
    T, C = oracle.encrypt(N, M)

    T_ = M[length + 1] ^^ C[length + 1]
    C_ = Block()
    sigma = Block.zero()
    for i in range(1, length):
        C_ = C_ + C[i]
        sigma = sigma ^^ M[i]
    C_ = C_ + (sigma ^^ C[length] ^^ Block.len(16))
    auth, M_ = oracle.decrypt(N, T_, C_)
    assert(auth == 'True')
    
    sigma = Block.zero()
    for i in range(i, length):
        sigma = sigma ^^ M[i]
    L = b2f(sigma ^^ M_[length] ^^ Block.len(16)) / (x ^ length)

    mappings = []
    for i in range(1, length):
        mappings.append((M[i] ^^ f2b((x ^ i) * L), C[i] ^^ f2b((x ^ i) * L)))

    return mappings

def specificMapping(Is):
    N, L = randomMapping(1)[0]
    L = b2f(L)

    n = len(Is)
    M = Block()
    for i in range(1, n + 1):
        M = M + (Is[i - 1] ^^ f2b((x ^ i) * L))
    M = M + Block.zero()
    T, C = oracle.encrypt(N, M)

    Os = []
    for i in range(1, n + 1):
        Os.append(C[i] ^^ f2b((x ^ i) * L))

    return Os

def forgery(N, M):
    L = specificMapping([N])[0]
    L = b2f(L)

    n = M.size()
    X = []
    sigma = Block.zero()
    for i in range(1, n):
        X.append(M[i] ^^ f2b((x ^ i) * L))
        sigma = sigma ^^ M[i]
    X.append(Block.len(16) ^^ f2b((x ^ n) * L))
    sigma = sigma ^^ M[n] ^^ f2b((x ^ n) * (x + 1) * L)
    X.append(sigma)

    Y = specificMapping(X)
    
    C = Block()
    for i in range(1, n):
        C = C + (Y[i - 1] ^^ f2b((x ^ n) * L))
    C = C + (Y[n - 1] ^^ M[n])
    T = Y[n]

    auth, M_ = oracle.decrypt(N, T, C)

    if auth == 'True':
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
