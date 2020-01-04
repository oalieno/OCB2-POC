#!/usr/bin/env python3
from pwn import remote
from block import Block

def log_function(description):
    def wrapperer(func):
        def wrapper(*args):
            print('-' * 20)
            print(description)
            print('-' * 20)
            results = func(*args)
            return results
        return wrapper
    return wrapperer

class Oracle:
    def __init__(self, ip, port):
        self.r = remote(ip, port)

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

    @log_function("Encryption Oracle")
    def encrypt(self, N, M):
        self.r.sendlineafter('> ', '1')
        self.sendData('nonce', N)
        self.sendData('plain', M)
        C = Block(self.getData('cipher'))
        T = Block(self.getData('tag'))
        print()
        return C, T

    @log_function("Decryption Oracle")
    def decrypt(self, N, C, T):
        self.r.sendlineafter('> ', '2')
        self.sendData('nonce', N)
        self.sendData('cipher', C)
        self.sendData('tag', T)
        auth = self.getData('auth', hex = False)
        M = None
        if auth == 'True':
            M = Block(self.getData('plain'))
        print()
        return auth == 'True', M
