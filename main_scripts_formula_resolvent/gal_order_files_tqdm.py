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

print(f"Generating all monic degree-{deg} polynomials with coefficients in [-{n}, {n}]...\n")

# Directory to hold output files
output_dir = f"galois_deg{deg}_range{n}"
os.makedirs(output_dir, exist_ok=True)

# Total number of coefficient combinations
total_combinations = (2*n + 1)**deg

# Wrap the product in tqdm for a progress bar
for coeffs in tqdm(product(range(-n, n + 1), repeat=deg), total=total_combinations, desc="Processing Polynomials"):
    # Create monic polynomial: x^deg + a_{deg-1}x^{deg-1} + ... + a_0
    f = x**deg + sum(c * x**i for i, c in enumerate(reversed(coeffs)))

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
