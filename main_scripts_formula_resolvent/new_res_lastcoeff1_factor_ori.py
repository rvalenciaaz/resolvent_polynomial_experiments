#!/usr/bin/env sage -python

from functions_resolvent_calculation import calc_vieta_sum_original
from sage.all import *
import sys
import csv
import os
import pandas as pd
from tqdm import tqdm

# ------------------------------
# Parse arguments
# ------------------------------
if len(sys.argv) < 3:
    print("Usage: sage analyze_all_groups_to_csv.sage <folder> <degree>")
    sys.exit(1)

folder = sys.argv[1]
degree = int(sys.argv[2])

# ------------------------------
# Get folder info from folder argument and create new output folder
# ------------------------------
folder_info = os.path.basename(os.path.normpath(folder))  # e.g., "galois_deg4_range15"
output_folder = f"output_last1_{folder_info}"
os.makedirs(output_folder, exist_ok=True)

# ------------------------------
# Declare variables and define symbols
# ------------------------------
max_vars = 100
var_list = [f"x{i}" for i in range(max_vars)] + [f"e{i}" for i in range(max_vars)]
var(var_list + ["n", "x", "T"])
var("a b c d e_coef f g h i_coef")

# ------------------------------
# Setup CSV Headers
# ------------------------------
vieta_terms = calc_vieta_sum_original(degree)
num_terms = len(vieta_terms)

fieldnames = (
    ["polynomial", "polynomial_reconstructed", "factors"]  # <-- Add the new "factors" column
    + [f"term_{i}" for i in range(num_terms)]
    + ["gcd", "zero_terms", "galois_group", "discriminant"]
)

# ------------------------------
# Open combined CSV file
# ------------------------------
combined_csv = os.path.join(output_folder, f"output_all_{folder_info}.csv")
combined_file = open(combined_csv, 'w', newline='')
combined_writer = csv.DictWriter(combined_file, fieldnames=fieldnames)
combined_writer.writeheader()

# ------------------------------
# Process each .txt file in the folder
# ------------------------------
txt_files = [f for f in os.listdir(folder) if f.endswith(".txt")]

for filename in tqdm(txt_files, desc="Processing files"):
    filepath = os.path.join(folder, filename)
    # Derive the Galois group name from the filename
    galois_group = os.path.splitext(filename)[0].split("=")[0].strip()

    group_csv = os.path.join(output_folder, f"output_last1_{galois_group}_{folder_info}.csv")
    group_file = open(group_csv, 'w', newline='')
    group_writer = csv.DictWriter(group_file, fieldnames=fieldnames)
    group_writer.writeheader()

    # Count lines in the file for a progress bar
    with open(filepath, 'r') as f:
        total_lines = sum(1 for _ in f)

    with open(filepath, 'r') as f:
        for poly_str in tqdm(f, total=total_lines, desc="Polynomials", leave=False):
            poly_str = poly_str.strip()
            if not poly_str:
                continue

            try:
                poly = SR(poly_str)
                coeffs = poly.coefficients(sparse=False)
                # Ensure correct length by padding with zeros if needed:
                coeffs = [0]*(degree + 1 - len(coeffs)) + coeffs

                if coeffs[0] != 1:
                    # Skip polynomials not ending in 1 (constant term != 1)
                    continue

                # Prepare substitutions for b, c, d, etc.
                named_coeffs = ['b','c','d','e_coef','f','g','h','i_coef']
                substitutions = {}
                for i in range(1, degree + 1):
                    varname = named_coeffs[degree - i]
                    substitutions[SR(varname)] = coeffs[i - 1]

                # Compute Vieta-derived expressions:
                vieta_sum_exprs = calc_vieta_sum_original(degree)
                repi = [expr.subs(substitutions).simplify().factor() for expr in vieta_sum_exprs]

                # Count zero terms, compute gcd
                repi_nonzero = [term for term in repi if term != 0]
                num_zeros = len(repi) - len(repi_nonzero)
                gcd_val = str(gcd(repi_nonzero)) if repi_nonzero else "undefined"

                # Discriminant
                R = PolynomialRing(QQ, 'x')
                xR = R.gen()
                poly_in_R = R(poly.subs(x=xR))
                discriminant_val = str(poly_in_R.discriminant())

                # Build a polynomial string from the substituted Vieta terms:
                # If num_terms = q+1, we treat term_0 as coefficient of x^q, etc.
                poly_terms_list = []
                for i_term in range(num_terms):
                    exponent = num_terms - 1 - i_term
                    coeff_str = str(repi[i_term])
                    if exponent == 0:
                        poly_terms_list.append(f"({coeff_str})")
                    else:
                        poly_terms_list.append(f"({coeff_str})*x^{exponent}")
                polynomial_reconstructed_str = " + ".join(poly_terms_list)

                # Also build the polynomial in R for factorization:
                # re-check we are in the same ring R so we can call factor().
                poly_reconstructed_R = sum(R(repi[i_term]) * (xR ** (num_terms - 1 - i_term))
                                           for i_term in range(num_terms))
                # Factorize and convert to string
                factors_str = str(poly_reconstructed_R.factor())

                # Prepare the row
                row = {
                    "polynomial": str(poly),
                    "polynomial_reconstructed": polynomial_reconstructed_str,
                    "factors": factors_str,  # <-- The new factorization info
                    "gcd": gcd_val,
                    "zero_terms": num_zeros,
                    "galois_group": galois_group,
                    "discriminant": discriminant_val,
                }

                # Fill in term_i columns
                for i_term in range(num_terms):
                    row[f"term_{i_term}"] = str(repi[i_term])

                group_writer.writerow(row)
                combined_writer.writerow(row)

            except Exception:
                # Skip rows that generate errors
                continue

    group_file.close()
    print(f"✅ Processed {filename} → {group_csv}")

combined_file.close()

# ------------------------------
# Export combined result to XLSX
# ------------------------------
try:
    df = pd.read_csv(combined_csv)
    combined_xlsx = os.path.join(output_folder, f"output_all_{folder_info}.xlsx")
    df.to_excel(combined_xlsx, index=False)
    print(f"\n📦 Combined XLSX → {combined_xlsx}")
except Exception as e:
    print("Error exporting to Excel:", e)

print(f"\n📦 Combined CSV → {combined_csv}")
