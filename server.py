#!/usr/bin/env python3
from ocb import OCB
from os import urandom

encrypt_nonces = []
decrypt_nonces = []

def getData(text):
    data = input(f'{text} = ').strip()
    return bytes.fromhex(data)

def sendData(text, data):
    if type(data) is bytes:
        print(f'{text} = {data.hex()}')
    else:
        print(f'{text} = {str(data)}')

def encrypt(ocb):
    N = getData('nonce')
    M = getData('plain')
    
    if N in encrypt_nonces:
        print('[you fuck up] nonce repeating')
        exit()
    encrypt_nonces.append(N)

    C, T = ocb.encrypt(N, M)

    sendData('cipher', C)
    sendData('tag', T)

def decrypt(ocb):
    N = getData('nonce')
    C = getData('cipher')
    T = getData('tag')
    
    if N in decrypt_nonces:
        print('[you fuck up] nonce repeating')
        exit()
    decrypt_nonces.append(N)
    
    auth, M = ocb.decrypt(N, C, T)
    sendData('auth', auth)
    if auth:
        sendData('plain', M)

def menu():
    print('1) Encrypt')
    print('2) Decrypt')
    print('3) Exit')

def main():
    ocb = OCB(urandom(16))
    while True:
        menu()
        option = input('> ')
        if option == '1':
            encrypt(ocb)
        elif option == '2':
            decrypt(ocb)
        else:
            return

main()
