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

def specificMappingInv(Is):
    N, L = randomMapping(1)[0]
    L = b2f(L)

    n = len(Is)
    C = Block()
    for i in range(1, n + 1):
        C = C + (Is[i - 1] ^^ f2b(x * L))
    for i in range(1, n + 1):
        C = C + (Is[i - 1] ^^ f2b((x ^ 2) * L))
    X = []
    X.append(Block.len(16) ^^ f2b((x ^ (2 * n + 1)) * L))
    X.append(f2b(x * L) ^^ f2b((x ^ (2 * n)) * L) ^^ f2b((x ^ (2 * n + 1) * (x + 1) * L)))
    Y = specificMapping(X)
    C = C + (Y[-2] ^^ Block.zero())
    T = Y[-1]
    auth, M = oracle.decrypt(N, T, C)

    Os = []
    for i in range(1, n + 1):
        Os.append(M[i] ^^ f2b(x * L))

    return Os

def recovery(N, T, C):
    L = specificMapping([N])[0]
    L = b2f(L)

    n = C.size()
    M = Block()
    if n == 1:
        Y = specificMapping([Block.len(16) ^^ f2b(x * L)])
        M += Y[0] ^^ C[1]
    elif n == 2:
        Y = specificMappingInv([C[1] ^^ f2b(x * L)])
        M += Y[0] ^^ f2b(x * L)
        Y = specificMapping([Block.len(16) ^^ f2b((x ^ 2) * L)])
        M += Y[0] ^^ C[2]
    else:
        for i in range(2, n):
            A, B = C[1], C[i]
            C[1] = B ^^ f2b(x * L) ^^ f2b((x ^ i) * L)
            C[i] = A ^^ f2b(x * L) ^^ f2b((x ^ i) * L)
            auth, M_ = oracle.decrypt(N, T, C)
            if i == 2:
                M += M_[i] ^^ f2b(x * L) ^^ f2b((x ^ i) * L)
            M += M_[1] ^^ f2b(x * L) ^^ f2b((x ^ i) * L)
            C[1], C[i] = A, B
        Y = specificMapping([Block.len(16) ^^ f2b((x ^ n) * L)])
        M += Y[0] ^^ C[n]

    auth, M_ = oracle.decrypt(N, T, C)

    if M.hex() == M_.hex():
        print(f'result = {green("Plaintext Recovered")}')
    else:
        print(f'result = {red("Plaintext Not Recovered")}')

N = Block.random(16)
M = Block.random(16 * 3)
T, C = oracle.encrypt(N, M)
print('-' * 10)
print('Plaintext Recovery')
print('-' * 10)
print(f'N = {N.hex()}')
print(f'M = {M.hex()}')
print()
recovery(N, T, C)
