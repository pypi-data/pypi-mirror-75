"""
================================================
== 	Filename: algorithm.py                    ==
== 	Author: Yi Lyu                            ==
==	Status: Complete                          ==
================================================

Contains common number theory algorithms

Library dependency:
    math
"""

import math

__all__ = ['fast_modular_multiply',
           'decompose_two',
           'gcd',
           'find_first_divisor',
           'euler_phi',
           'inverse_mod',
           'search_non_residue',
           'tonelli_shanks'
          ]

def fast_modular_multiply(g, k, p):
    """Calculates the value g^k mod p
    
    Args:
        g: an integer representing the base
        k: an integer representing the exponent
        p: an integer (prime number)
        
    Returns:
        an integer representing g^k mod p

    """
    u = g
    y = 1
    while k != 0:
        if k % 2 == 1:
            y = y * u % p
        u = u * u % p
        k //= 2
    return y

def decompose_two(p):
    """Decomposes p into p - 1 = q * 2^s
    
    Args:
        p: an integer representing a prime number
        
    Results:
        p: an integer representing q above
        k: an integer representing the exponent of 2

    """
    k = 0
    while p % 2 == 0:
        k += 1
        p //= 2
    return p, k

def gcd(a, b):
    """greatest common divisor
    
    Calculates the greatest common divisor with
    Euclidean algorithm.
    example:
        
        val = gcd(33, 6)
        print(val) ## 3
    
    Args:
        a: an int representing the first argument
        b: an int representing the second argument
    
    Returns:
        an int representing the greatest common divisor

    """
    if (a < b):
        a, b = b, a
    temp = -1
    while a % b != 0:
        temp = a
        a = b
        b = temp % b
    return b

def find_first_divisor(N):
    """Finds the first divisor of N
    
    Args:
        N: an integer to be factored

    Returns:
        an integer representing the first divisor of N

    """
    for i in range(2, int(math.sqrt(N)) + 1):
        if N % i == 0:
            return i
    return N

def euler_phi(N):
    """Calculates the Euler Phi function
    
    Args:
        N: an integer
        
    Results:
        an integer representing phi(N)
    
    """
    result = N
    divisor = 1
    p = find_first_divisor(N)
    while p != N:
        while N % p == 0:
            N //= p
        result *= p - 1
        divisor *= p
        p = find_first_divisor(N)
    if p != 1:
        return result * (p - 1) // (divisor * p)
    else:
        return result // divisor
    
def inverse_mod(x, p):
    """Calculates the inverse of x mod p
    
    Args:
        x: an integer
        p: an integer (prime number)
        
    Returns:
        an integer representing the inverse of x mod p

    """
    return pow(x, p - 2, p)

def search_non_residue(p):
    """Find a non residue of p between 2 and p
    
    Args:
        p: a prime number
        
    Returns:
        a integer that is not a quadratic residue of p
        or -1 if no such number exists 

    """
    for z in range(2, p):
        if pow(z, (p - 1) // 2, p) == p - 1:
            return z
    return -1

def tonelli_shanks(n, p):
    """Tonelli Shanks algorithm
    
    Solves the equation x^2 = n mod p
    
    Args:
        n: an integer representing the base
        p: an integer (prime number)
        
    Returns:
        two integers representing the possible x
        -1, -1 if n is not a quadratic residue of p

    """
    if pow(n, (p - 1) // 2, p) != 1:
        return -1, -1
    
    q, s = decompose_two(p - 1)
    
    z = search_non_residue(p)
    
    if z == -1:
        return -1, -1
    
    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) // 2, p)
    
    while t != 1:
        i = 0
        div = False
        while (not div):
            i += 1
            t = int(math.pow(t, 2)) % p
            if (t % p == 1):
                div = True
        b = pow(c * c, m - i - 1, p)
        c = pow(b, 2, p)
        t = (t * c) % p
        r = (r * b) % p
        m = i
    
    return r, p - r
