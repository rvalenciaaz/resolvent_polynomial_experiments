#!/usr/bin/env sage -python

import sys
import os
from itertools import product
from sage.all import PolynomialRing, QQ
from tqdm import tqdm

# Parse command-line arguments
n = int(sys.argv[1]) if len(sys.argv) > 1 else 5       # coefficient range: -n to n
deg = int(sys.argv[2]) if len(sys.argv) > 2 else 3     # polynomial degree

# Define a polynomial ring in x over Q
R = PolynomialRing(QQ, 'x')
x = R.gen()

print(f"Generating all monic degree-{deg} polynomials with constant term = 1 and other coefficients in [-{n}, {n}]...\n")

# Directory to hold output files
output_dir = f"galois_deg{deg}_range{n}_constant1"
os.makedirs(output_dir, exist_ok=True)

# We only vary the deg-1 middle coefficients (x^{deg-1} through x^1),
# since the polynomial is monic (leading coefficient = 1) and we set the constant term to 1.
total_combinations = (2*n + 1)**(deg - 1)

# Wrap the product in tqdm for a progress bar
for coeffs in tqdm(
    product(range(-n, n + 1), repeat=deg - 1),
    total=total_combinations,
    desc="Processing Polynomials"
):
    # coeffs corresponds to (a_{deg-1}, a_{deg-2}, ..., a_1)
    # so we build:  x^deg + a_{deg-1} x^{deg-1} + ... + a_1 x + 1
    f = x**deg + sum(c * x**i for i, c in enumerate(reversed(coeffs), start=1)) + 1

    # Check if irreducible
    if f.is_irreducible():
        try:
            G = f.galois_group(pari_group=True)
            group_name = G.label()

            # Write polynomial to corresponding file
            filename = os.path.join(output_dir, f"{group_name}.txt")
            with open(filename, 'a') as file:
                file.write(f"{f}\n")

        except Exception as e:
            # Optionally log this
            print(f"Error computing Galois group for f(x) = {f}: {e}")
