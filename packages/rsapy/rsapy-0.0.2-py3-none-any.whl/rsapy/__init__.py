__version__ = '0.0.1'
__author__ = 'Sandra Mattar'
__email__ = 'sandrawmattar@gmail.com'
__url__ = 'https://pypi.org/project/rsapy'

import random
from random import randrange
from math import gcd, log
from collections import namedtuple
import binascii
hexlify, unhexlify = binascii.hexlify, binascii.unhexlify
from base64 import *
import string
import pickle
import idlelib
import os
import string

Key = namedtuple('Key', 'exponent modulus')
KeyPair = namedtuple('KeyPair', 'public private')

def genvigkey(keylen):
    return ''.join((random.choice(string.printable) for _ in range(keylen)))

def vigencode(text, key):
    d = ''
    if __debug__:
        assert len(key) >= len(text)
    else:
        raise AssertionError('key must be longer or as long as text for secure \
encryption. ')
        return
    
    for idx in range(min((len(text), len(key)))):
        d += chr(ord(text[idx]) + ord(key[idx]))

    return d

def vigdecode(text, key):
    d = ''
    if __debug__:
        assert len(key) >= len(text)
    else:
        raise Exception('key must be longer or as long as text for secure \
encryption. ')
        return
    
    for idx in range(min((len(text), len(key)))):
        d += chr(ord(text[idx]) - ord(key[idx]))

    return d

def isprime(n, k = 30):
    if n <= 3:
        return n == 2 or n == 3
    n1 = n-1
    s, d = 0, n1
    while not d & 1:
        s, d = s + 1, d >> 1
    assert 2 ** s * d == n1 and d & 1

    for _ in range(k):
        a = randrange(2, n1)
        x = pow(a, d, n)
        if x in (1, n1):
            continue
        for _ in range(s - 1):
            x = x ** 2 % n
            if x == 1:
                return False
            if x == n1:
                break
        else:
            return False
    return True

def multinv(mod, var):
    x, lx = 0, 1
    a, b = mod, var
    while b:
        a, q, b = b, a // b, a % b
        x, lx = lx - q * x, x
    result = (1 - lx * mod) // var
    if result < 0:
        result += mod
    assert 0 <= result < mod and var * result % mod == 1
    return result

def randprime(n = 10**8):
    p = 1
    while not isprime(p):
        p = random.randrange(n)
    return p

def genkey(n = 10**8, public = None):
    prime1 = randprime(n)
    prime2 = randprime(n)
    composite = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    if public is None:
        private = None
        while True:
            private = randrange(totient)
            if gcd(private, totient) == 1:
                break
        public = multinv(totient, private)
    else:
        private = multinv(totient, public)
    assert public * private % totient == gcd(public, totient) == \
           gcd(private, totient) == 1
    assert pow(pow(1234567, public, composite), private, composite) == 1234567
    return KeyPair(Key(public, composite), Key(private, composite))

def genprikey(public):
    prime1, prime2 = get_prime_factors(public.modulus)
    composite = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    private = multinv(totient, public.exponent)
    return Key(private, composite)

def isrelprime(x, y):
    return gcd(x, y) == 1

def randrelprime(x):
    p = randrange(x)
    while not isrelprime(x, p):
        p = randrange(x)
    return p

def encode(msg, pubkey):
    chunksize = int(log(pubkey.modulus, 256))
    outchunk = chunksize + 1
    outfmt = '%%0%dx' % (outchunk * 2,)
    bmsg = msg if isinstance(msg, bytes) else msg.encode('utf-8')
    result = []
    for start in range(0, len(bmsg), chunksize):
        chunk = bmsg[start:start + chunksize]
        chunk += b'\x00' * (chunksize - len(chunk))
        plain = int(hexlify(chunk), 16)
        coded = pow(plain, *pubkey)
        bcoded = unhexlify((outfmt % coded).encode())
        result.append(bcoded)
        
    result = b''.join(result)
    result = b85encode(result)
    result = result.decode()
    return result

def decode(msg, prikey):
    msg = msg.encode()
    msg = b85decode(msg)
    
    chunksize = int(log(prikey.modulus, 256))
    outchunk = chunksize + 1
    outfmt = '%%0%dx' % (chunksize * 2,)
    result = []
    for start in range(0, len(msg), outchunk):
        bcoded = msg[start: start + outchunk]
        coded = int(hexlify(bcoded), 16)
        plain = pow(coded, *prikey)
        chunk = unhexlify((outfmt % plain).encode())
        result.append(chunk)
    return b''.join(result).rstrip(b'\x00').decode('utf-8')

def key2str(key):
    return ':'.join(hex(_) for _ in key)

def str2key(str):
    return Key(*(int(_, 16) for _ in str.split(':')))

def get_prime_factors(N):
    factors = list()
    divisor = 2
    while(divisor <= N):
        if (N % divisor) == 0:
            factors.append(divisor)
            N = N/divisor
        else:
            divisor += 1
    return factors

##def genok(numkeys, keylen = 10**8):
##    o = [_+1 for _ in range(numkeys)]
##    random.shuffle(o)
##
####    k = [genkey(keylen) for _ in range(numkeys)]
##    k = []
##    _ = 0
##    for _ in tqdm.tqdm_gui(range(numkeys)):
##        k.append(genkey(keylen))
##        if _ == 0:
##            plt.get_current_fig_manager().window.title('RSA Status')
####            plt.get_current_fig_manager().window.iconbitmap(
####                default = os.path.join(os.path.dirname(idlelib.__file__),
####                                       'Icons', 'idle.ico'))
##        _ += 1
##
##    plt.get_current_fig_manager().window.withdraw()
##        
##    random.shuffle(k)
##
##    return o, k

def processok(order, keys):
    k = []
    for x in order:
        k.append(keys[x-1])
    return order, k

def encodeorder(msg, processedkeys):
    for key in tqdm.tqdm_gui(processedkeys):
        if key == processedkeys[0]:
            plt.get_current_fig_manager().window.title('RSA Status')
        msg = encode(msg, key.public if isinstance(key, KeyPair) else key)
    plt.get_current_fig_manager().window.withdraw()
    return msg

def decodeorder(msg, processedkeys):
    processedkeys = [_ for _ in processedkeys]
    processedkeys.reverse()
    for key in tqdm.tqdm_gui(processedkeys):
        if key == processedkeys[0]:
            plt.get_current_fig_manager().window.title('RSA Status')
        msg = decode(msg, key.private if isinstance(key, KeyPair) else key)
    plt.get_current_fig_manager().window.withdraw()
    return msg

def pubfromkeys(keys):
    return [key.public for key in keys]

def prifromkeys(keys):
    return [key.private for key in keys]

def fmtrsa(rsakey):
    return fmtdata(key2str(rsakey))

def unfmtrsa(data):
    return str2key(unfmtdata(data))

def fmtdata(data):
    return pickle.dumps(b85encode(pickle.dumps(data)))

def unfmtdata(data):
    return pickle.loads(b85decode(pickle.loads(data)))

##def fmtrsaok(order, keys):
####    keys = pubfromkeys(keys)
##    keys = [key2str(key) for key in keys]
##    keys = [pickle.dumps(b85encode(pickle.dumps(data))) for data in keys]
##    order = [pickle.dumps(b85encode(pickle.dumps(data))) for data in order]
##    data = order, keys
##    return pickle.dumps(b85encode(pickle.dumps(data)))
##
##def unfmtrsaok(data):
##    data = pickle.loads(b85decode(pickle.loads(data)))
##    order, keys = data
##    order = [pickle.loads(b85decode(pickle.loads(data))) for data in order]
##    keys = [pickle.loads(b85decode(pickle.loads(data))) for data in keys]
##    keys = [str2key(str) for str in keys]
##    return order, keys
