#!/usr/bin/env python3
# -*- coding: utf‑8 -*-
#
#  test_cascade_generic.py    –  example for the “stop‑at‑any‑degree” cascade
# ---------------------------------------------------------------------------
from sage.all import solve, SR, var
from functions_resolvent_cascade import iterate_common_calc_to_degree, ele_dict, vietas_dict

def main():
    # -----------------------------------------------------------------------
    # Settings
    # -----------------------------------------------------------------------
    start_degree   = 4      # the original polynomial is degree‑5
    stop_degree    = 3      # tell the cascade to halt at a cubic
    variable_name  = "Z"    # symbol used for that cubic

    # -----------------------------------------------------------------------
    # 1) Produce the reduced polynomial
    # -----------------------------------------------------------------------
    cubic = iterate_common_calc_to_degree(start_degree,
                                          stop_degree,
                                          var_name=variable_name)
    print(f"Monic degree‑{stop_degree} polynomial from cascade:")
    print("   ", cubic, "\n")
    print(cubic.subs(vietas_dict(start_degree)))
    # -----------------------------------------------------------------------
    # 2) Solve it symbolically
    # -----------------------------------------------------------------------
    Z     = SR.var(variable_name)
    roots = solve(cubic == 0, Z, solution_dict=True)
    print("Roots in terms of eₖ:")
    for i, sol in enumerate(roots, 1):
        print(f"   r{i} =", sol[Z])
    print()

    # -----------------------------------------------------------------------
    # 3) Expand eₖ into the 5 original roots x0…x4 and simplify
    # -----------------------------------------------------------------------
    #subs_dict = ele_dict(start_degree)   # degree‑5 expansions
    #print("After expanding eₖ into x0…x4:")
    #for i, sol in enumerate(roots, 1):
        #expanded = sol[Z].simplify().subs(subs_dict).simplify().factor()
        #print(f"   r{i} =", expanded)

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
