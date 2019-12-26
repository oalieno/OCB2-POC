#!/usr/bin/env python3
from remote import Remote
from block import Block

class Oracle:
    def __init__(self, ip, port):
        self.r = Remote(ip, port)

    def __del__(self): 
        self.r.sendline('3')

    def getData(self, text, hex = True):
        self.r.recvuntil(f'{text} = ')
        if hex:
            data = bytes.fromhex(self.r.recvline().strip().decode())
            print(f'[+] get {text} = {data.hex()}')
        else:
            data = self.r.recvline().strip().decode()
            print(f'[+] get {text} = {data}')
        return data

    def sendData(self, text, data):
        self.r.sendlineafter(f'{text} = ', data.hex())
        print(f'[+] send {text} = {data.hex()}')

    def encrypt(self, N, M):
        print('-' * 10)
        print('Encryption Oracle')
        print('-' * 10)
        self.r.sendlineafter('> ', '1')
        self.sendData('nonce', N)
        self.sendData('plain', M)
        T = Block(self.getData('tag'))
        C = Block(self.getData('cipher'))
        print()
        return T, C

    def decrypt(self, N, T, C):
        print('-' * 10)
        print('Decryption Oracle')
        print('-' * 10)
        self.r.sendlineafter('> ', '2')
        self.sendData('nonce', N)
        self.sendData('tag', T)
        self.sendData('cipher', C)
        auth = self.getData('auth', hex = False)
        M = None
        if auth == 'True':
            M = Block(self.getData('plain'))
        print()
        return auth, M
