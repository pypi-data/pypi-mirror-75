"""
================================================
== 	Filename: elgamal_pkc.py
== 	Author: Yi Lyu
==	Status: Complete
================================================

Implements the Elgamal Public Key Cryptography

Depends on the hardness of Diffie Hellman Problem.
Example:
    
    >>> elgamal_pkc = ElgamalPKC(467, 2)
    >>> elgamal_pkc.set_secret_key(153)
    >>> elgamalPKC.decrypt(elgamalPKC.encrypt(331))
    331

Library dependency:
    random
"""

from random import seed
from random import randint
from .. import algorithm as algo

seed(1)

__all__ = ['ElgamalPKC']

class ElgamalPKC:
    """Elgamal public key cryptography
    
    Attributes:
        public_key: the public key
        g: the base
        _secret_key: the secret key
    """
    def __init__(self, p, g):
        """ Initializes the Elgamal PKC """
        self.public_key = p
        self.g = g
    
    def get_public_key(self):
        """ gets the public key """
        return self.public_key
    
    def get_g(self):
        """ gets the base """
        return self.g
    
    def set_secret_key(self, a):
        """ sets the secret key """
        self._secret_key = a
        
    def encrypt(self, m):
        """Encrypts the message
        
        Args:
            m: an integer representing the message
            
        Returns:
            a tuple of two elements representing the
            encrypted message
        """
        p = self.public_key
        A = self._get_a()
        key = randint(2, p)
            
        c1 = algo.fast_modular_multiply(self.g, key, p)
        c2 = (m * algo.fast_modular_multiply(A, key, p)) % p
        return c1, c2
    
    def decrypt(self, pair):
        """Decrypts the message
        
        Args:
            pair: a tuple of two represneting the encrypted message
        
        Returns:
            an integer representing the original message
        """
        p = self.public_key
        a = self._secret_key
        return self._decrypt_helper(p, a, pair[0], pair[1])
    
    ## Helper Function
    def _decrypt_helper(self, p, a, c1, c2):
        return c2 * algo.fast_modular_multiply(c1, p - 1 - a, p) % p

    def _get_a(self):
        """ gets a = g^k """
        return algo.fast_modular_multiply(self.g, self._secret_key, self.public_key)
