#!/usr/bin/env python3
from ocb.aes import AES
from ocb import OCB
from base64 import b64decode, b64encode
from os import urandom

aes = AES(128)
ocb = OCB(aes)
key = urandom(16)
ocb.setKey(key)

def getData(text):
    data = input(f'{text} = ').strip()
    return bytes.fromhex(data)

def sendData(text, data, hex = True):
    if hex:
        print(f'{text} = {data.hex()}')
    else:
        print(f'{text} = {str(data)}')

def encrypt():
    N = getData('nonce')
    M = getData('plain')
    ocb.setNonce(N)
    T, C = ocb.encrypt(M, '')
    sendData('tag', T)
    sendData('cipher', C)

def decrypt():
    N = getData('nonce')
    T = getData('tag')
    C = getData('cipher')
    ocb.setNonce(N)
    auth, M = ocb.decrypt('', C, T)
    sendData('auth', auth, hex = False)
    if auth:
        sendData('plain', M)

def menu():
    print('1) Encrypt')
    print('2) Decrypt')
    print('3) Exit')

def main():
    while True:
        menu()
        option = input('> ')
        if option == '1':
            encrypt()
        elif option == '2':
            decrypt()
        else:
            return

main()
