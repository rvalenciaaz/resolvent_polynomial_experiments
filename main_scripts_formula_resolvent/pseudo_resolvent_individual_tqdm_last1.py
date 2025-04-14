#!/usr/bin/env sage -python

from functions_resolvent_calculation import calc_vieta_sum
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
# Setup CSV Headers based on the fixed number of Vieta terms.
# We assume calc_vieta_sum(degree) returns a list with fixed length.
# ------------------------------
vieta_terms = calc_vieta_sum(degree)
num_terms = len(vieta_terms)
fieldnames = (
    ["polynomial"]
    + [f"term_{i}" for i in range(num_terms)]
    + ["gcd", "zero_terms", "galois_group", "discriminant"]
)

# ------------------------------
# Open combined CSV file for streaming writing in the output folder
# ------------------------------
combined_csv = os.path.join(output_folder, f"output_all_{folder_info}.csv")
combined_file = open(combined_csv, 'w', newline='')
combined_writer = csv.DictWriter(combined_file, fieldnames=fieldnames)
combined_writer.writeheader()

# ------------------------------
# Process each file in the folder, streaming lines and writing rows immediately
# ------------------------------
txt_files = [f for f in os.listdir(folder) if f.endswith(".txt")]

for filename in tqdm(txt_files, desc="Processing files"):
    filepath = os.path.join(folder, filename)
    # Only consider the part of the filename before the first equal sign.
    galois_group = os.path.splitext(filename)[0].split("=")[0].strip()

    # Open per-group CSV file inside the output folder
    group_csv = os.path.join(output_folder, f"output_last1_{galois_group}_{folder_info}.csv")
    group_file = open(group_csv, 'w', newline='')
    group_writer = csv.DictWriter(group_file, fieldnames=fieldnames)
    group_writer.writeheader()

    # Count the number of lines in the file for progress reporting.
    with open(filepath, 'r') as f:
        total_lines = sum(1 for _ in f)

    # Reopen the file for processing with a tqdm progress bar.
    with open(filepath, 'r') as f:
        for poly_str in tqdm(f, total=total_lines, desc="Polynomials", leave=False):
            poly_str = poly_str.strip()
            if not poly_str:
                continue
            try:
                poly = SR(poly_str)
                coeffs = poly.coefficients(sparse=False)
                # Ensure correct number of coefficients by padding with zeros:
                coeffs = [0] * (degree + 1 - len(coeffs)) + coeffs

                if coeffs[0] != 1:
                    # Skip non-monic polynomials.
                    continue

                # Prepare substitutions for named coefficients:
                named_coeffs = ['b', 'c', 'd', 'e_coef', 'f', 'g', 'h', 'i_coef']
                substitutions = {}
                for i in range(1, degree + 1):
                    varname = named_coeffs[i - 1] if i - 1 < len(named_coeffs) else f"c{i}"
                    substitutions[SR(varname)] = coeffs[i]

                # Compute Vieta-derived terms (assumed constant in number for fixed degree)
                vieta_sum_exprs = calc_vieta_sum(degree)
                repi = [expr.subs(substitutions).simplify().factor() for expr in vieta_sum_exprs]
                repi_nonzero = [term for term in repi if term != 0]
                num_zeros = len(repi) - len(repi_nonzero)

                # Compute GCD and discriminant:
                gcd_val = str(gcd(repi_nonzero)) if repi_nonzero else "undefined"

                R = PolynomialRing(QQ, 'x')
                xR = R.gen()
                poly_in_R = R(poly.subs(x=xR))
                discriminant_val = str(poly_in_R.discriminant())

                # Build the row with exactly num_terms columns for terms.
                row = {
                    "polynomial": str(poly),
                    "gcd": gcd_val,
                    "zero_terms": num_zeros,
                    "galois_group": galois_group,
                    "discriminant": discriminant_val
                }
                for i in range(num_terms):
                    row[f"term_{i}"] = str(repi[i]) if i < len(repi) else ""

                # Write the row to both the group and the combined CSV files immediately.
                group_writer.writerow(row)
                combined_writer.writerow(row)

            except Exception:
                # Skip rows that generate errors (optionally log the exception).
                continue

    group_file.close()
    print(f"✅ Processed {filename} → {group_csv}")

combined_file.close()

# ------------------------------
# Combined XLSX export (if desired)
# ------------------------------
try:
    df = pd.read_csv(combined_csv)
    combined_xlsx = os.path.join(output_folder, f"output_all_{folder_info}.xlsx")
    df.to_excel(combined_xlsx, index=False)
    print(f"\n📦 Combined XLSX → {combined_xlsx}")
except Exception as e:
    print("Error exporting to Excel:", e)

print(f"\n📦 Combined CSV → {combined_csv}")
