"""
================================================
== 	Filename: elliptic_curve.py               ==
== 	Author: Yi Lyu                            ==
==	Status: Complete                          ==
================================================

Defines the elliptic curve in mathematics and
provides some cryptographic functions related to it.

Library dependency:
    sys
"""
import sys
from .. import algorithm as algo

__all__ = ['EllipticCurve']

class EllipticCurve:
    """Elliptic curve class
    
    Provides basic operations needed when working
    with Elliptic curve (y^2 = x^3 + Ax + B).
    
    Attributes:
        A: a number (int) representing the coefficient of x above.
        B: a number (int) representing the coefficient of 1 above.
        p: an integer (prime number) indicating the field the elliptic
        curve is over (F_p).
        _zero_point: an two-element array representing the additive identity.
    
    """
    def __init__(self, A, B, p):
        """ Initializes the ellitpic curve """
        self.A = A
        self.B = B
        self.p = p
        self._zero_point = [sys.maxsize, -sys.maxsize]
        
    def add(self, P, Q):
        """Adds two points on the ellitpic curve
        
        Args:
            P: an array representing the coordinates
            of the first point.
            Q: an array representing the coordinates
            of the second point.
            
        Returns:
            an array representing the coordinates
            of P + Q
        """
        x1, y1 = P[0], P[1]
        x2, y2 = Q[0], Q[1]
        if x1 == self._zero_point[0] and y1 == self._zero_point[1]:
            return Q
        if x1 == x2 % self.p and y1 == (self.p - y2) % self.p:
            return self._zero_point
        if P != Q:
            slope = (y1 - y2) * self._inverse(x1 - x2) % self.p
        else:
            slope = (3 * x1 * x1 + self.A) * self._inverse(2 * y1) % self.p
        x3 = (slope * slope - x1 - x2) % self.p
        return [x3, (slope * (x1 - x3) - y1) % self.p]
    
    def multiply(self, P, n):
        """Calculates the value Q = nP
        
        Calculates the value Q = nP using double and add algorithm
        
        Args:
            P: an array representing the coordinates of the point
            n: an integer representing the coefficient
            
        Returns:
            an array representing the coordinates of Q = nP
        """
        if n == 0:
            return self._zero_point
        elif n == 1:
            return P
        else:
            val = self.add(self.multiply(P, n // 2), self.multiply(P, n // 2))
            if n % 2 == 0:
                return val
            else:
                return self.add(val, P)
        
    def is_on_curve(self, P):
        """ Determines whether a point P is on the curve """
        x, y = P[0], P[1]
        lhs = (y * y) % self.p
        rhs = (x ** 3 + self.A * x + self.B) % self.p
        return lhs == rhs
            
    def list_points(self):
        """ Lists all the points on the curve """
        result = []
        result.append(self._zero_point)
        for i in range(self.p):
            for j in range(self.p):
                if self.is_on_curve([i, j]):
                    result.append([i, j])
        return result

    ## Helper Functions
    def _inverse(self, x):
        start = 1
        while x < 0:
            x += self.p
        d = algo.gcd(x, self.p)
        if d != 1:
            print("p can be factored into {0} and {1}".format(d, self.p // d))
            sys.exit()
        while (start * x % self.p != 1):
            start += 1
        return start
