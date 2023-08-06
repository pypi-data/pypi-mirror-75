"""Contains factorization algorithms and related ones

Have implemented the following algorithms:
    miller_rabin: the renowned Miller Rabin Test
    p1_factorize: Pollard's p - 1 algorithm

Example:
    >>> N = 247
    >>> p1_factorize(N)
    13
    >>> miller_rabin(35, 3)
    1
"""
import math
from .. import algorithm as algo

__all__ = ['miller_rabin', 'p1_factorize']

def miller_rabin(n, x):
    """Checks whether x is a Miller Rabin witness of n
    
    Args:
        n: an integer that is potentially prime
        x: an integer that is potentially a Miller Rabin witness
    
    Returns:
        1: It is a Miller Rabin witness and n is composite
        0: It is not a Miller Rabin witness

    """
    a = x
    if n % 2 == 0 or algo.gcd(a, n) > 1:
        return 1
    k, q = algo.decompose_two(n - 1)
    a = pow(a, k, n)
    if a == 1:
        return 0
    for i in range(0, q):
        if a == n - 1:
            return 0
        a = pow(a, 2, n)
    print("Composite")
    return 1
    

def p1_factorize(N):
    """Factorize N using Pollard's p - 1 algorithm
    
    Args:
        N: an integer to be factored
        
    Returns:
        an integer that is a factor of N
        or -1 if N is a prime

    """
    a = 2
    for i in range(2, int(math.sqrt(N))):
        a = pow(a, i, N)
        d = algo.gcd(a - 1, N)
        if d < N and d > 1:
            return d
    return -1
