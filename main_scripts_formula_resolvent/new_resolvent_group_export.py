#!/usr/bin/env sage -python

from functions_resolvent_calculation import calc_vieta_sum
from sage.all import *
import sys
import csv
import os

# ------------------------------
# Parse arguments
# ------------------------------
if len(sys.argv) < 3:
    print("Usage: sage analyze_group_polys_to_csv.sage <filename> <degree>")
    sys.exit(1)

filename = sys.argv[1]
degree = int(sys.argv[2])

# ------------------------------
# Declare needed variables
# ------------------------------
max_vars = 100
var_list = [f"x{i}" for i in range(max_vars)] + [f"e{i}" for i in range(max_vars)]
var(var_list + ["n", "x", "T"])
var("a b c d e_coef f g h i_coef")

# Infer Galois group from filename
galois_group = os.path.splitext(os.path.basename(filename))[0]

# ------------------------------
# Load polynomials
# ------------------------------
with open(filename, 'r') as f:
    polys = [line.strip() for line in f if line.strip()]

# ------------------------------
# Process and collect rows
# ------------------------------
rows = []
max_terms = 0

for poly_str in polys:
    try:
        poly = SR(poly_str)
        coeffs = poly.coefficients(sparse=False)
        coeffs = [0] * (degree + 1 - len(coeffs)) + coeffs

        if coeffs[0] != 1:
            continue

        named_coeffs = ['b', 'c', 'd', 'e_coef', 'f', 'g', 'h', 'i_coef']
        substitutions = {}

        for i in range(1, degree + 1):
            varname = named_coeffs[i - 1] if i - 1 < len(named_coeffs) else f"c{i}"
            substitutions[SR(varname)] = coeffs[i]

        substitutions[x0] = 1

        vieta_sum = calc_vieta_sum(degree)
        repi = [expr.subs(substitutions).simplify().factor() for expr in vieta_sum]
        repi_nonzero = [term for term in repi if term != 0]
        num_zeros = len(repi) - len(repi_nonzero)
        gcd_val = str(gcd(repi_nonzero)) if repi_nonzero else "undefined"

        row = {
            "polynomial": str(poly),
            "gcd": gcd_val,
            "zero_terms": num_zeros,
            "galois_group": galois_group
        }

        for i, term in enumerate(repi):
            row[f"term_{i}"] = str(term)

        max_terms = max(max_terms, len(repi))
        rows.append(row)

    except Exception:
        continue

# ------------------------------
# Prepare CSV headers
# ------------------------------
fieldnames = ["polynomial"] + [f"term_{i}" for i in range(max_terms)] + ["gcd", "zero_terms", "galois_group"]

# ------------------------------
# Write to CSV
# ------------------------------
output_csv = f"output_{galois_group}_deg{degree}.csv"
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        # Fill in missing term_i columns with empty string if needed
        for i in range(max_terms):
            if f"term_{i}" not in row:
                row[f"term_{i}"] = ""
        writer.writerow(row)

print(f"✅ Exported {len(rows)} results to: {output_csv}")
