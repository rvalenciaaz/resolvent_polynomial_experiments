#!/usr/bin/env sage -python

from sage.all import PolynomialRing, QQ

# 1. Create a polynomial ring R in one variable x over the rationals QQ.
#    In the Sage REPL, we often do "R.<x> = PolynomialRing(QQ)", but in Python
#    we must do it in two steps:

R = PolynomialRing(QQ, 'x')   # 'x' is the variable name
x = R.gen()                   # x is now the generator for R

# 2. Define the polynomial of interest (e.g., f = x^5 - 2).
f = x**5 - 2

# 3. Compute the Galois group of the polynomial f over Q.
G = f.galois_group(pari_group=True)

# 4. Print the result.
print("Polynomial:", f)
print("Galois group:", G)
