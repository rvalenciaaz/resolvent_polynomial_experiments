from functions_resolvent_calculation import calc_rootis_original
from sage.all import var, RR
import numpy as np
import matplotlib.pyplot as plt
import os

# Set up variables
max_j = 6  # Adjust this to control how many values of j you try
samples = 100000

# Create the symbolic variables only once
x_vars = ["x" + str(i) for i in range(100)]
var(x_vars)

# Ensure output directory
output_dir = "root_ratio_histograms"
os.makedirs(output_dir, exist_ok=True)

# Loop over different j values
for j in range(3, max_j + 1):
    print(f"Processing j = {j}...")
    cr=calc_rootis_original(j)
    # Get the symbolic expression for ratio
    ratio_expr = cr[1] / cr[0]
    vars_needed = x_vars[:j]

    # Compile fast lambda function using Sage
    ratio_func = ratio_expr.function(*[var(v) for v in vars_needed])

    # Sample from normal distribution
    X = np.random.normal(loc=0, scale=1, size=(samples, j))

    # Evaluate the symbolic function over all samples
    values = []
    for row in X:
        try:
            val = ratio_func(*row)
            values.append(float(RR(val)))
        except Exception:
            # In case of division by zero or other issues
            continue

    # Convert to numpy array
    values = np.array(values)

    # Histogram
    plt.figure(figsize=(6, 4))
    plt.hist(values, bins=300, density=True, alpha=0.7, range=(
        np.mean(values) - 20, # - 4*np.std(values),
        np.mean(values) + 20 # + 4*np.std(values)
    ))
    plt.title(f"Histogram of root ratio for j = {j}")
    plt.xlabel("root[1] / root[0]")
    plt.ylabel("Density")
    plt.grid(True)

    # Save histogram
    plt.tight_layout()
    plt.savefig(f"{output_dir}/histogram_ori_j{j}.png")
    plt.close()

print("Done. Histograms saved in", output_dir)
