#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_cascade_generic.py  –  “stop‑at‑any‑degree” cascade
#  -----------------------------------------------------------------------
#  Generates the degree‑3 resolvent produced by the generic cascade and
#  finds its roots strictly through Vieta’s formulas, allowing a
#  non‑monic leading term.
#  -----------------------------------------------------------------------

from sage.all import solve, SR, var
from functions_resolvent_cascade import (
    iterate_common_calc_to_degree,  # cascade driver
    ele_dict,                       # expands eₖ  →  x₀…x₄
    vietas_dict                     # expands eₖ  →  coefficients of the original poly
)

def main() -> None:
    # -------------------------------------------------------------------
    # Settings
    # -------------------------------------------------------------------
    start_degree  = 4     # the original polynomial is degree‑5
    stop_degree   = 3     # stop the cascade at a cubic
    variable_name = "Z"   # symbol used for that cubic

    # -------------------------------------------------------------------
    # 1) Produce the reduced polynomial
    # -------------------------------------------------------------------
    cubic = iterate_common_calc_to_degree(
        start_degree,
        stop_degree,
        var_name=variable_name
    )

    print(f"\nDegree‑{stop_degree} cascade polynomial:")
    print("   ", cubic, "\n")

    print("After substituting elementary symmetric coefficients eₖ:")
    print("   ", cubic.subs(vietas_dict(start_degree)), "\n")

    # -------------------------------------------------------------------
    # 2) Recover its three roots via Vieta’s system (non‑monic version)
    # -------------------------------------------------------------------
    Z = SR.var(variable_name)

    A  = cubic.coefficient(Z, 3)          # leading coefficient (≠ 1 in general)
    b2 = cubic.coefficient(Z, 2)
    b1 = cubic.coefficient(Z, 1)
    b0 = cubic.coefficient(Z, 0)

    # Unknown roots
    r1, r2, r3 = var("r1 r2 r3")

    # Vieta relations for the general cubic  A Z³ + b₂ Z² + b₁ Z + b₀ = 0
    eqs = [
        r1 + r2 + r3 + b2 / A == 0,      #  r₁ + r₂ + r₃ = −b₂/A
        r1*r2 + r1*r3 + r2*r3 - b1 / A == 0,   #  Σ rᵢ rⱼ =  b₁/A
        r1*r2*r3 + b0 / A == 0           #  r₁ r₂ r₃ = −b₀/A
    ]

    solutions = solve(eqs, r1, r2, r3, solution_dict=True)

    print("Roots obtained with Vieta’s symmetric system (in terms of eₖ):")
    for i, sol in enumerate(solutions, 1):
        print(f"   solution {i}:  r1 = {sol[r1]},  r2 = {sol[r2]},  r3 = {sol[r3]}")
    print()

    # -------------------------------------------------------------------
    # 3) (Optional) Expand the eₖ into the five original roots x₀…x₄
    # -------------------------------------------------------------------
    # subs_dict = ele_dict(start_degree)          # degree‑5 expansions
    # print("After expanding eₖ into x0…x4:")
    # for i, sol in enumerate(solutions, 1):
    #     expanded = tuple(
    #         sol[r].subs(subs_dict).simplify().factor() for r in (r1, r2, r3)
    #     )
    #     print(f"   solution {i}:  (r1, r2, r3) = {expanded}\n")

# -------------------------------------------------------------------------
if __name__ == "__main__":
    main()
