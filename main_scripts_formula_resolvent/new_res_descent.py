#!/usr/bin/env sage -python

from functions_resolvent_calculation import calc_vieta_sum
from sage.all import *
import sys
import csv
import os
import pandas as pd

# ------------------------------
# Parse arguments
# ------------------------------
if len(sys.argv) < 3:
    print("Usage: sage analyze_all_groups_to_csv.sage <folder> <degree>")
    sys.exit(1)

folder = sys.argv[1]
degree = int(sys.argv[2])

# ------------------------------
# Declare needed variables
# ------------------------------
max_vars = 100
var_list = [f"x{i}" for i in range(max_vars)] + [f"e{i}" for i in range(max_vars)]
var(var_list + ["n", "x", "T"])
var("a b c d e_coef f g h i_coef")

# Track all data across all files
all_rows = []
max_terms_global = 0

# ------------------------------
# Process each file in the folder
# ------------------------------
for filename in os.listdir(folder):
    if not filename.endswith(".txt"):
        continue

    filepath = os.path.join(folder, filename)
    galois_group = os.path.splitext(filename)[0]

    with open(filepath, 'r') as f:
        polys = [line.strip() for line in f if line.strip()]

    rows = []
    max_terms = 0

    for poly_str in polys:
        try:
            poly = SR(poly_str)
            coeffs = poly.coefficients(sparse=False)
            coeffs = [0] * (degree + 1 - len(coeffs)) + coeffs

            if coeffs[0] != 1:
                continue  # Skip non-monic

            named_coeffs = ['b', 'c', 'd', 'e_coef', 'f', 'g', 'h', 'i_coef']
            substitutions = {}

            for i in range(1, degree + 1):
                varname = named_coeffs[i - 1] if i - 1 < len(named_coeffs) else f"c{i}"
                substitutions[SR(varname)] = coeffs[i]

            substitutions[x0] = 1

            # Vieta terms
            vieta_sum = calc_vieta_sum(degree)
            repi = [expr.subs(substitutions).simplify().factor() for expr in vieta_sum]
            repi_nonzero = [term for term in repi if term != 0]
            num_zeros = len(repi) - len(repi_nonzero)

            # GCD
            if repi_nonzero:
                gcd_expr = gcd(repi_nonzero)
                gcd_val = str(gcd_expr)
            else:
                gcd_val = "undefined"

            # Discriminant of the polynomial
            R = PolynomialRing(QQ, 'x')
            xR = R.gen()
            poly_in_R = R(poly.subs(x=xR))
            discriminant_val = str(poly_in_R.discriminant())

            # Optional expressions based on a, b, c, d from repi
            expr_zeros = ""
            b2_3ac = bc_9ad = c2_3bd = ""
            try:
                a_r, b_r, c_r, d_r = repi[:4]
                b2_3ac = (b_r**2 - 3*a_r*c_r).simplify()
                bc_9ad = (b_r*c_r - 9*a_r*d_r).simplify()
                c2_3bd = (c_r**2 - 3*b_r*d_r).simplify()
                zero_exprs = [b2_3ac == 0, bc_9ad == 0, c2_3bd == 0]
                expr_zeros = sum(zero_exprs)
            except Exception:
                b2_3ac = bc_9ad = c2_3bd = "err"
                expr_zeros = ""

            # Create row
            row = {
                "polynomial": str(poly),
                "gcd": gcd_val,
                "zero_terms": num_zeros,
                "galois_group": galois_group,
                "discriminant": discriminant_val,
                "b2_minus_3ac": str(b2_3ac),
                "bc_minus_9ad": str(bc_9ad),
                "c2_minus_3bd": str(c2_3bd),
                "expr_zeros": expr_zeros
            }

            for i, term in enumerate(repi):
                row[f"term_{i}"] = str(term)

            max_terms = max(max_terms, len(repi))
            max_terms_global = max(max_terms_global, len(repi))

            rows.append(row)
            all_rows.append(row)

        except Exception:
            continue

    if not rows:
        continue

    # ------------------------------
    # Save per-group CSV
    # ------------------------------
    fieldnames = (
        ["polynomial"]
        + [f"term_{i}" for i in range(max_terms)]
        + ["gcd", "zero_terms", "galois_group", "discriminant",
           "b2_minus_3ac", "bc_minus_9ad", "c2_minus_3bd", "expr_zeros"]
    )

    output_csv = f"output_{galois_group}_deg{degree}.csv"
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            for i in range(max_terms):
                if f"term_{i}" not in row:
                    row[f"term_{i}"] = ""
            writer.writerow(row)

    print(f"✅ Processed {filename} → {output_csv} ({len(rows)} entries)")

# ------------------------------
# Combined CSV and Excel export
# ------------------------------
if all_rows:
    combined_fieldnames = (
        ["polynomial"]
        + [f"term_{i}" for i in range(max_terms_global)]
        + ["gcd", "zero_terms", "galois_group", "discriminant",
           "b2_minus_3ac", "bc_minus_9ad", "c2_minus_3bd", "expr_zeros"]
    )

    combined_csv = f"output_all_deg{degree}.csv"
    combined_xlsx = f"output_all_deg{degree}.xlsx"

    # Write CSV
    with open(combined_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=combined_fieldnames)
        writer.writeheader()
        for row in all_rows:
            for i in range(max_terms_global):
                if f"term_{i}" not in row:
                    row[f"term_{i}"] = ""
            writer.writerow(row)

    # Write XLSX
    df = pd.DataFrame(all_rows, columns=combined_fieldnames)
    df.to_excel(combined_xlsx, index=False)

    print(f"\n📦 Combined CSV → {combined_csv}")
    print(f"📦 Combined XLSX → {combined_xlsx}")
else:
    print("⚠️ No valid data found.")
