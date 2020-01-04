from block import *

def randomMapping(oracle, n):
    N = Block.random(16)
    M = Block.random(n * 16) + Block.len(16) + Block.random(16)
    C, T = oracle.encrypt(N, M)

    S = Block.zero()
    C_ = Block()
    T_ = M[n + 1] ^ C[n + 1]
    for i in range(n):
        C_ += C[i]
        S ^= M[i]
    C_ += (S ^ C[n] ^ Block.len(16))
    auth, M_ = oracle.decrypt(N, C_, T_)
    assert(auth)
    
    S = Block.zero()
    for i in range(n):
        S ^= M[i]
    L = (S ^ M_[n] ^ Block.len(16)).half(n + 1) 

    mappings = []
    for i in range(n):
        mappings.append((M[i] ^ L.double(i + 1), C[i] ^ L.double(i + 1)))

    return mappings

def specificMapping(oracle, Is):
    N, L = randomMapping(oracle, 1)[0]

    n = len(Is)
    M = Block()
    for i in range(n):
        M += (Is[i] ^ L.double(i + 1))
    M += Block.zero()
    C, T = oracle.encrypt(N, M)

    Os = []
    for i in range(n):
        Os.append(C[i] ^ L.double(i + 1))

    return Os

def specificMappingInv(oracle, Is):
    N, L = randomMapping(oracle, 1)[0]

    n = len(Is)
    C = Block()
    for i in range(n):
        C += Is[i - 1] ^ L.double()
    for i in range(n):
        C += Is[i - 1] ^ L.double(2)
    
    X = []
    X.append(Block.len(16) ^ L.double(2 * n + 1))
    X.append(L.double() ^ L.double(2 * n) ^ L.double(2 * n + 1) ^ L.double(2 * n + 2))
    Y = specificMapping(oracle, X)
    C += Y[-2] ^ Block.zero()
    T = Y[-1]
    auth, M = oracle.decrypt(N, C, T)

    Os = []
    for i in range(n):
        Os.append(M[i] ^ L.double())

    return Os

