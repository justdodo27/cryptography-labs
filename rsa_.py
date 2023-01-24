import random as rn
import math
import sympy

# random prime number
def rand_prime(ub, other=None):
    other = tuple() if other is None else other
    while True:
        x = rn.randint(2, ub)
        if sympy.isprime(x) and not x in other:
            return x
            
def generate_relatively_prime(ub, relative=1):
    while True:
        x = rn.randint(2, ub)
        if sympy.isprime(x) and  math.gcd(x, relative) == 1:
            return x

def generate_keys(p: int, q: int):
    n = p*q
    phi = (p-1)*(q-1)

    e = generate_relatively_prime(2**32, relative=phi)
    d = pow(e, -1, mod=phi)

    return (e, n), (d, n)

def encrypt_message(key, msg):
    msg_bytes = bytes(msg, encoding='utf-8')
    return [pow(c, key[0], key[1]) for c in msg_bytes]

def decrypt_message(key, msg):
    decrypted_bytes = [pow(c, key[0], key[1]) for c in msg]
    text = bytes(decrypted_bytes).decode('utf-8')
    return text