# OCB2-POC

Proof of Concept of [2019 attack](https://eprint.iacr.org/2019/311.pdf)

## Resource

Some resource about OCB2

### Paper

* [2001 OCB1 - proposal to NIST](https://eprint.iacr.org/2001/026.pdf)
* [2001 OCB1 Download Link 1](https://dl.acm.org/citation.cfm?doid=501983.502011)
* [2001 OCB1 Download Link 2](https://web.cs.ucdavis.edu/~rogaway/papers/ocb-full.pdf)
* [2004 OCB2 Download Link 1](https://link.springer.com/chapter/10.1007%2F978-3-540-30539-2_2)
* [2004 OCB2 Download Link 2](https://web.cs.ucdavis.edu/~rogaway/papers/offsets.pdf)
* [2011 OCB3](https://link.springer.com/chapter/10.1007%2F978-3-642-21702-9_18)
* [2018 attack](https://eprint.iacr.org/2018/1040.pdf)
* [2018 attack - by other researcher](https://eprint.iacr.org/2018/1090.pdf)
* [2018 attack - by other researcher](https://eprint.iacr.org/2018/1087.pdf)
* [2019 attack](https://eprint.iacr.org/2019/311.pdf)
* [A Concrete Security Treatment of Symmetric Encryption](https://web.cs.ucdavis.edu/~rogaway/papers/sym-enc.pdf)

### Standard

* [rfc7253 OCB3](https://tools.ietf.org/html/rfc7253)
* [ISO OCB2](https://www.iso.org/standard/46345.html)

### Tutorial

* [OCB Author Official Tutorial](https://web.cs.ucdavis.edu/~rogaway/ocb/ocb-faq.htm#versions)
* [2011 Author Slides](https://web.cs.ucdavis.edu/~rogaway/ocb/11-01-378r2-I-OCB_Mode.pdf)
* [stackexchange](https://crypto.stackexchange.com/questions/63626/what-is-the-new-attack-on-ocb2-and-how-does-it-work)
* [youtube](https://www.youtube.com/watch?v=QKwGsnZ9Bqw)

### Implementation

* [python cryptodome - ocb3 mode](https://pycryptodome.readthedocs.io/en/latest/src/cipher/modern.html#ocb-mode)
* [pyOCB - ocb2 mode](https://github.com/kravietz/pyOCB)

## POC

### Server

```
socat TCP-LISTEN:20000,fork EXEC:./server.py
```

### Minimal Forgery

```
$ ./minimal-forgery.py
----------
Encryption Oracle
----------
[+] send nonce = 6682614d5f0092dbf976ca81943827a1
[+] send plain = 0000000000000000000000000000008043b3f10da5db32ca00f6ba84fdbc85c1
[+] get tag = 69e71259f2aed354f12d6fc2103c3fc9
[+] get cipher = 00c760940398b6897ce96d3d4e4b430f835e2ea1ba8a79a283c9047915275d0b

----------
Decryption Oracle
----------
[+] send nonce = 6682614d5f0092dbf976ca81943827a1
[+] send tag = c0eddfac1f514b68833fbefde89bd8ca
[+] send cipher = 00c760940398b6897ce96d3d4e4b438f
[+] get auth = True
[+] get plain = 0ccb5fe3c17860bf9165716f4c23bdfa

result = Authenticated
```

### Longer Message Forgery

```
$ ./longer-forgery.py 5
----------
Encryption Oracle
----------
[+] send nonce = de1e6f14fdef93c9a8bf54c12a243eb3
[+] send plain = 39228efc5d6d1b68ee9ebcd8ac867044fa4a6585d4fedc10a00969abd86f5057c9eb318696284de53aa570c3ee8e9f3a9d906b43dbd707f529d3b6405837f3320000000000000000000000000000008000d4ceb422729d2586c54b92d076d565
[+] get tag = 9f9ccbd1bfe7c364c3ea5d053517a1ba
[+] get cipher = 577ad4c98e0b16d81622d1fa9b825b2552d2d272c42ac83eb3d2b38f8d530644c95ffe294b3f3fbab708411af4adedfe6a558ec83188c504419a8f40cc3fde6f36582375c59faae5a7bfe189e33c7d2fa87cc7755095ff76084ffe5b1d26d147

----------
Decryption Oracle
----------
[+] send nonce = de1e6f14fdef93c9a8bf54c12a243eb3
[+] send tag = a8a809c172e762538e8ab5c9cd500422
[+] send cipher = 577ad4c98e0b16d81622d1fa9b825b2552d2d272c42ac83eb3d2b38f8d530644c95ffe294b3f3fbab708411af4adedfe6a558ec83188c504419a8f40cc3fde6fa14b92c901f3278dfa5ef279216c31b4
[+] get auth = True
[+] get plain = 39228efc5d6d1b68ee9ebcd8ac867044fa4a6585d4fedc10a00969abd86f5057c9eb318696284de53aa570c3ee8e9f3a9d906b43dbd707f529d3b6405837f3329b43665eb6b27842c54e90c292543b3c

result = Authenticated
```

### Universal Forgery

SageMath version 8.8, Release Date: 2019-06-26 Using Python 3.7.3.  
You can try [sagemath docker](https://hub.docker.com/r/sagemath/sagemath)

```
$ sage ./universal-forgery.sage
----------
Universal Forgery
----------
N = f6240662bce61382f0987db561ad5a0f
M = 35e6b533c36f9200ff201dee08b15274

----------
Encryption Oracle
----------
[+] send nonce = c7a063b53cf1889ba69b44833429f313
[+] send plain = d872b92627927a80ab02d5f56c99a20500000000000000000000000000000080e1eb94304094decfead5cd07ac469eef
[+] get tag = 2ba87b6fe31ec77832acb5d433c83d14
[+] get cipher = fe7b58b7abc1e4c4c27c9a01000087ceb1f508388d7f009687861dba05956c49603485a1d4f81ef80262e23661ceee38

----------
Decryption Oracle
----------
[+] send nonce = c7a063b53cf1889ba69b44833429f313
[+] send tag = 81df1191946cc037e8b72f31cd8870d7
[+] send cipher = fe7b58b7abc1e4c4c27c9a01000087ce6987b11eaaed7a162c84c84f690ccecc
[+] get auth = True
[+] get plain = d872b92627927a80ab02d5f56c99a205e864520af88dd4f5d26ea1768e5de059

----------
Encryption Oracle
----------
[+] send nonce = c079ccb0481dadba17b4efb49dfb836b
[+] send plain = 3ac45c21347a747e0d0d3d34836817c800000000000000000000000000000000
[+] get tag = c189c34da46cda6b9e4a507e7e44e585
[+] get cipher = cf2f7ef61a789fd279d596b475d69b24899a42844207e624507262f17bc53dc0

----------
Encryption Oracle
----------
[+] send nonce = 746d63f578a37370c4367252d4dad4e4
[+] send plain = e9cd3b4931265e644c4ef9402a41317a000000000000000000000000000000807e47c2d2c1f0cbbc9fe0ee4ad6cb5ef2
[+] get tag = 6278746d737441c8ca6ced5d59276d64
[+] get cipher = 4f7a55c7bb944666528bc72510a9eded99febead7a0a80b1962332c824820eba589b43198e5908a45944416f3b55b2ac

----------
Decryption Oracle
----------
[+] send nonce = 746d63f578a37370c4367252d4dad4e4
[+] send tag = 26dc81cb4fa9c318c6a4af25ed9eec5e
[+] send cipher = 4f7a55c7bb944666528bc72510a9eded703385e44b2cded5da6dcb880ec33f40
[+] get auth = True
[+] get plain = e9cd3b4931265e644c4ef9402a41317a4f690b2c6ac989398b63ff50b25e99ab

----------
Encryption Oracle
----------
[+] send nonce = 3a9f237b9cd1b5caafd87a48664ee511
[+] send plain = 3fced281090eabcc6abb2431976bdecd4de5595af4bb35c522d7f9e60841432800000000000000000000000000000000
[+] get tag = 59809c4dc1d20dabf3e82bf40131e05c
[+] get cipher = 1c454d604eb67efdfe2da9dbdb6e688e0d0511db90bfdce1832194cfc8ad3701b29438adedc7ddeb9ef9b276b4edd7ab

----------
Decryption Oracle
----------
[+] send nonce = f6240662bce61382f0987db561ad5a0f
[+] send tag = 7da4260fc9316bc34754847aba35d017
[+] send cipher = 11f363b9a11eb76c63373c6f6a934971
[+] get auth = True
[+] get plain = 35e6b533c36f9200ff201dee08b15274

result = Authenticated
```

### Plaintext Recovery

```
$ sage plaintext-recovery.sage
----------
Encryption Oracle
----------
[+] send nonce = 861a6e94d8cc667a64c8e12db0412bb1
[+] send plain = 6c57b3858044d4d51594a6815b5639c59b8b4aa78c831ac7a1d5887fe14ee5b46abe60be59aa54cf3799d4dbd85f7e8c
[+] get tag = 3f1f53ca6b9ee985b75c189c13596aa5
[+] get cipher = 97c204333030879fe9c0513bf0d225a615c5abbfc23034e0054276a746d4411d5045f91788c1902204d12b169d8435a0

----------
Plaintext Recovery
----------
N = 861a6e94d8cc667a64c8e12db0412bb1
T = 3f1f53ca6b9ee985b75c189c13596aa5
C = 97c204333030879fe9c0513bf0d225a615c5abbfc23034e0054276a746d4411d5045f91788c1902204d12b169d8435a0

----------
Encryption Oracle
----------
[+] send nonce = aba587ee1f07f7802dcbe9d2f52d6de2
[+] send plain = 05a63dcd7989095eef763df8be1d2945000000000000000000000000000000803ab1ab7726a6c7f33943341487706ecc
[+] get tag = 8cee5b581735ed6980fc9d9efa2d33a5
[+] get cipher = ca847e0b6dd7034dcf82a5e62e474c2684e70c6443cfc59a1e10178900cc85d158302045daa6de5f6fbb1fae4cc18ea7

----------
Decryption Oracle
----------
[+] send nonce = aba587ee1f07f7802dcbe9d2f52d6de2
[+] send tag = 62818b32fc0019ac56f82bbacbb1e06b
[+] send cipher = ca847e0b6dd7034dcf82a5e62e474c26814131a93a46ccc4f1662a71bed1ac14
[+] get auth = True
[+] get plain = 05a63dcd7989095eef763df8be1d2945ecc79358e209d690ad69519b6ee804d3

----------
Encryption Oracle
----------
[+] send nonce = 7116ea87b44966b9ce798bc95667bfce
[+] send plain = fa733c1798e2bf2fb9d2c6823c3a9e6c00000000000000000000000000000000
[+] get tag = 6a6daf45a826f61ef43b0366483ede29
[+] get cipher = c03716c1ed4b32a8de0bd6b9f6b4ff620f2bb9a8fc104277cef84630c186d529

----------
Decryption Oracle
----------
[+] send nonce = 861a6e94d8cc667a64c8e12db0412bb1
[+] send tag = 3f1f53ca6b9ee985b75c189c13596aa5
[+] send cipher = 9c0032302d6c4cee0f2650d25877ff161e079dbcdf6cff91e3a4774eee719bad5045f91788c1902204d12b169d8435a0
[+] get auth = True
[+] get plain = 124ed32863df62c9abb1ae0affed5bbfe5922a0a6f18acdb1ff080f445f587ce6abe60be59aa54cf3799d4dbd85f7e8c

----------
Encryption Oracle
----------
[+] send nonce = cef6d94892279e71bf32a709dca1b120
[+] send plain = 0785f5770b306a926fcaca3882dc68d000000000000000000000000000000080f5f96b73af8f8d36365391fea516269b
[+] get tag = a535f0d64bfb1b5c867ec630674eca6e
[+] get cipher = d3f1d2f0a8a79bf5066332d873cae78ea61db6f317dd651fa80f0bea8d8e062e65099674d668e8f09a90ee1abd0996d9

----------
Decryption Oracle
----------
[+] send nonce = cef6d94892279e71bf32a709dca1b120
[+] send tag = 90f0fd0779e765c6acc37fe4181fb042
[+] send cipher = d3f1d2f0a8a79bf5066332d873cae78ea19843841ced0f8dc7c5c1d20f526e7e
[+] get auth = True
[+] get plain = 0785f5770b306a926fcaca3882dc68d0465f55ab6c183c206659969b90b6ab52

----------
Encryption Oracle
----------
[+] send nonce = 2768a51938a441cb6b0364690be90951
[+] send plain = 04cb27285d483eb01ddab1a023855b7a00000000000000000000000000000000
[+] get tag = 1afbb254eeb153e55da26dbb603e8ee0
[+] get cipher = dcc29c94e70ca5b5361dc6deb02447b5086bd5a90bb20fdfac2320cae3b1ef45

----------
Decryption Oracle
----------
[+] send nonce = 861a6e94d8cc667a64c8e12db0412bb1
[+] send tag = 3f1f53ca6b9ee985b75c189c13596aa5
[+] send cipher = 97c204333030879fe9c0513bf0d225a615c5abbfc23034e0054276a746d4411d5045f91788c1902204d12b169d8435a0
[+] get auth = True
[+] get plain = 6c57b3858044d4d51594a6815b5639c59b8b4aa78c831ac7a1d5887fe14ee5b46abe60be59aa54cf3799d4dbd85f7e8c

result = Plaintext Recovered
```
