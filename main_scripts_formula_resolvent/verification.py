#!/usr/bin/env sage -python

import sys
import os
from sage.all import PolynomialRing, QQ

# Check filename
if len(sys.argv) < 2:
    print("Usage: sage verify_galois.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
expected_group = os.path.splitext(os.path.basename(filename))[0]

# Set up polynomial ring
R = PolynomialRing(QQ, 'x')
x = R.gen()

print(f"Verifying Galois groups in file: {filename} (Expected: {expected_group})\n")

with open(filename, 'r') as file:
    for line_num, line in enumerate(file, start=1):
        poly_str = line.strip()
        if not poly_str:
            continue

        try:
            # Convert string to polynomial
            f = R(poly_str)

            # Compute Galois group
            G = f.galois_group(pari_group=True)
            actual_group = G.label()

            status = "✓" if actual_group == expected_group else f"✗ (Got: {actual_group})"
            print(f"[Line {line_num}] {f}    →    {actual_group} {status}")

        except Exception as e:
            print(f"[Line {line_num}] Error with '{poly_str}': {e}")
