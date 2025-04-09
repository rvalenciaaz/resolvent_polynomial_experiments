#!/usr/bin/env sage -python

from sage.all import PolynomialRing, QQ
import sys
from itertools import product

# Parse command-line arguments
n = int(sys.argv[1]) if len(sys.argv) > 1 else 5       # coefficient range: -n to n
deg = int(sys.argv[2]) if len(sys.argv) > 2 else 3     # polynomial degree

# Define a polynomial ring in x over Q
R = PolynomialRing(QQ, 'x')
x = R.gen()

print(f"Iterating over all monic degree-{deg} polynomials with coefficients in [-{n}, {n}]\n")

# Generate all combinations of coefficients [a_{d-1}, ..., a_0]
# (degree d means d coefficients after leading x^d)
for coeffs in product(range(-n, n + 1), repeat=deg):
    # Build polynomial: x^d + a_{d-1}x^{d-1} + ... + a_0
    f = x**deg + sum(c * x**i for i, c in enumerate(reversed(coeffs)))

    # Check irreducibility
    if f.is_irreducible():
        try:
            G = f.galois_group(pari_group=True)
            symbol = G.label()
            print(f"f(x) = {f}    Galois group: {symbol}")
        except Exception as e:
            print(f"f(x) = {f}    [Error computing Galois group: {e}]")
