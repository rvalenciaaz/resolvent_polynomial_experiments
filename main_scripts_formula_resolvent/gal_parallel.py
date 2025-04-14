#!/usr/bin/env sage -python

import sys
import os
import gc
from itertools import product
from multiprocessing import Pool, Lock, cpu_count

# Sage imports
from sage.all import PolynomialRing, QQ

# -----------------------------------------------------------
# GLOBALS (accessible by all worker processes)
# -----------------------------------------------------------
WRITE_LOCK = None      # A lock for writing to files safely
OUTPUT_DIR = None      # The output directory path

def parse_arguments():
    """
    Parse command line arguments:
       1) n   -> range [-n..n]
       2) deg -> polynomial degree
    Defaults: n=5, deg=3
    """
    args = sys.argv[1:]
    if len(args) >= 1:
        n = int(args[0])
    else:
        n = 5
    if len(args) >= 2:
        deg = int(args[1])
    else:
        deg = 3
    return n, deg

def process_one_polynomial(coeffs_and_deg):
    """
    Worker function for a single polynomial's coefficients.
    
    1. Build the monic polynomial f(x) = x^deg + ... from coeffs.
    2. Check irreducibility.
    3. If irreducible, compute Galois group, then write the polynomial
       to a file named after the Galois group label.
       - If the group label contains "=", we only take the text before "=".
    4. Force garbage collection to minimize memory growth.
    
    Arguments:
      coeffs_and_deg: tuple (coeffs, deg)
         - coeffs is a tuple (a_{deg-1}, ..., a_0)
         - deg is the polynomial degree
    """
    coeffs, deg = coeffs_and_deg

    # Create the polynomial ring and variable
    R = PolynomialRing(QQ, 'x')
    x = R.gen()

    # 1. Build monic polynomial
    #    f(x) = x^deg + sum(a_{deg-1 - i} * x^i for i in range(deg))
    f = x**deg
    for i in range(deg):
        f += coeffs[deg - 1 - i] * x**i

    # 2. Check irreducibility
    if not f.is_irreducible():
        gc.collect()
        return

    # 3. Compute Galois group
    try:
        G = f.galois_group(pari_group=True)
        group_label = G.label()
    except Exception:
        gc.collect()
        return

    # If the group label contains '=', split and take only the part before '='
    if '=' in group_label:
        group_label = group_label.split('=', 1)[0].strip()

    # 4. Write polynomial to file under lock
    global WRITE_LOCK, OUTPUT_DIR
    with WRITE_LOCK:
        filename = os.path.join(OUTPUT_DIR, f"{group_label}.txt")
        with open(filename, 'a') as out_f:
            out_f.write(str(f) + "\n")

    # Force garbage collection after each polynomial to reduce memory
    gc.collect()

def main():
    # 1. Parse arguments
    n, deg = parse_arguments()
    print(f"Generating all monic degree-{deg} polynomials with coefficients in [-{n}, {n}]...")

    # 2. Create output directory
    global OUTPUT_DIR
    OUTPUT_DIR = f"galois_deg{deg}_range{n}"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 3. Create a lock for file writes
    global WRITE_LOCK
    WRITE_LOCK = Lock()

    # 4. Prepare the generator of coefficient tuples
    #    Each element is (a_{deg-1}, ..., a_0)
    coeffs_gen = product(range(-n, n+1), repeat=deg)

    # 5. Wrap each polynomial in a (coeffs, deg) tuple
    #    so the worker knows the degree as well
    tasks = ((coeffs, deg) for coeffs in coeffs_gen)

    # 6. Set up multiprocessing pool
    #    If memory is tight, reduce the number of processes below 8.
    num_procs = 8
    # num_procs = cpu_count()  # Use all cores if you prefer (and have enough RAM)
    pool = Pool(processes=num_procs)

    # 7. Distribute work. We use imap_unordered with a chunksize=1
    #    so each polynomial is handled independently.
    for _ in pool.imap_unordered(process_one_polynomial, tasks, chunksize=1):
        pass
    # We don’t gather results; they’re written directly to disk.

    # 8. Close and join the pool
    pool.close()
    pool.join()

    print(f"Done. Wrote results to directory '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    main()
