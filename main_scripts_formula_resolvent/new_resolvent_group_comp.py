#!/usr/bin/env sage -python

from functions_resolvent_calculation import calc_vieta_sum
from sage.all import *
import sys

# ------------------------------
# Parse arguments
# ------------------------------
if len(sys.argv) < 3:
    print("Usage: sage analyze_group_polys.sage <filename> <degree>")
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

# ------------------------------
# Load polynomials
# ------------------------------
with open(filename, 'r') as f:
    polys = [line.strip() for line in f if line.strip()]

# ------------------------------
# Process each polynomial
# ------------------------------
for poly_str in polys:
    try:
        poly = SR(poly_str)
        coeffs = poly.coefficients(sparse=False)
        coeffs = [0] * (degree + 1 - len(coeffs)) + coeffs

        # Skip non-monic
        if coeffs[0] != 1:
            continue

        named_coeffs = ['b', 'c', 'd', 'e_coef', 'f', 'g', 'h', 'i_coef']
        substitutions = {}

        for i in range(1, degree + 1):
            varname = named_coeffs[i - 1] if i - 1 < len(named_coeffs) else f"c{i}"
            substitutions[SR(varname)] = coeffs[i]

        substitutions[x0] = 1
        print(f"\nPolynomial = {poly_str}")
        vieta_sum = calc_vieta_sum(degree)
        repi = [expr.subs(substitutions).simplify().factor() for expr in vieta_sum]

        print("Terms:", repi)

        # Compute GCD of non-zero terms only
        repi_nonzero = [term for term in repi if term != 0]
        if repi_nonzero:
            print("GCD:", gcd(repi_nonzero), "\n")
        else:
            print("GCD: undefined (all zero terms)\n")

    except Exception:
        continue
