from numpy.random import randint
import numpy as np
from sympy import isprime
from fractions import Fraction

map = lambda xs, f: [f(x) for x in xs]
join = lambda xs, sep: sep.join(xs)

def poly_eval(A, x):
    X = np.array([x**i for i in range(len(A))])
    y = np.sum(A*X)
    return y

def lagr_interp(X):
    num, den = np.ones_like(X), np.ones_like(X)
    for i, xi in enumerate(X):
        for j, xj in enumerate(X):
            if i == j: continue
            num[i] *= xj
            den[i] *= xj - xi
    return [Fraction(a, b) for a, b in zip(num, den)]

def shamir_e(secret, n, t, p):
    assert p > secret
    assert p > n
    assert isprime(p)
    #t-1 losowych liczb a1, a2, …, at-1 i a0=sekret
    A = [secret] + list(randint(0, p, size=t-1))
    
    res0 = []
    for i, x in enumerate(A): res0.append(f'a_{i} = {x}')
    
    #algorytm rozdzielający
    X = np.arange(n) + 1
    Y = [poly_eval(A, x) for x in X]
    
    # pary (x,y) to kolejne udziały
    res1 = []
    for x, y in zip(X, Y): res1.append(f's_{x} = f({x}) mod p = {y: 12d} mod {p} = {y % p}')
    
    res2 = join([f'{x},{y % p}' for x, y in zip(X, Y)], ';')

    return res0, res1, res2

def shamir_d(keys, p):
    X, Y = np.array([map(x.split(','), int) for x in keys.split(';')]).T
    L = lagr_interp(X)
    res0 = L[0]
    S = np.sum(Y * L) % p # modulo is distributive
    
    # pretty print results
    res1 = []
    for i in range(len(X)): res1.append(f'y_{i}*l_{i} = {Y[i]: 6d} * {L[i]} = {Y[i] * L[i]}')
    res2 = S

    return res0, res1, res2