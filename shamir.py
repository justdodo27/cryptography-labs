from numpy.random import randint
import numpy as np
from sympy import isprime
from fractions import Fraction
from scipy.interpolate import lagrange


def poly_eval(A, x):
    X = np.array([x**i for i in range(len(A))])
    y = np.sum(A*X)
    return y

def shamir_e(secret, n, t, p):
    #t-1 losowych liczb a1, a2, …, at-1 i a0=sekret
    A = [secret] + list(randint(0, p, size=t-1))
    
    res0 = []
    for i, x in enumerate(A): res0.append(f'a_{i} = {x}')
    
    #algorytm rozdzielający
    X = np.arange(n) + 1
    Y = [poly_eval(A, x) for x in X]
    
    res2 = [(x, y % p) for x, y in zip(X, Y)]
    
    return res0, res2

def shamir_d(keys):
    mat = np.array((keys))
    X = mat[:, 0]
    Y = mat[:, 1]
    L = lagrange(X, Y)
    print(L.coefficients)
    secret = round(L.coefficients[-1])

    return secret