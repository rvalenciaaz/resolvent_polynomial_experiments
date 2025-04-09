#!/usr/bin/env sage -python

from sage.all import PolynomialRing, QQ
import sys

# Get user-defined range n (defaults to 5 if not provided)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 5

# Define a polynomial ring in x over Q
R = PolynomialRing(QQ, 'x')
x = R.gen()

print(f"Iterating over all cubic polynomials x^3 + b x^2 + c x + d, with b, c, d in [-{n}, {n}]\n")

# Loop over all combinations of b, c, d
for b in range(-n, n + 1):
    for c in range(-n, n + 1):
        for d in range(-n, n + 1):
            f = x**3 + b*x**2 + c*x + d

            # Check irreducibility
            if f.is_irreducible():
                # Compute Galois group and extract PARI group name
                G = f.galois_group(pari_group=True)
                symbol = G.label()  # Correct way to get the name like "S3", "A3"
                print(f"f(x) = {f}    Galois group: {symbol}")
