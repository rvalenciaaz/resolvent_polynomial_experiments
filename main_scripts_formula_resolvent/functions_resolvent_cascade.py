#!/usr/bin/env python3
# -*- coding: utf‑8 -*-
#
#  cascade_common_calc.py   (generalised version)
# ---------------------------------------------------------------------------
from sage.all import *

# ----------------------------------------------------------------------------
#  Symbolic “global” setup  (unchanged)
# ----------------------------------------------------------------------------
var_list = [f"x{i}" for i in range(100)] + [f"e{i}" for i in range(100)]
var(var_list + ["n", "x", "T"])
var("a b c d e_coef f g h i_coef")

x0 = SR.var("x0")
_e = SymmetricFunctions(QQ).e()

# ----------------------------------------------------------------------------
#  Elementary‑symmetric helpers  (unchanged)
# ----------------------------------------------------------------------------
def ele_dict(deg):
    return {eval(f"e{k}"): _e[k].expand(deg) for k in range(deg + 1)}

def polexp(n):
    return sum(((-1) ** k) * eval(f"e{k}") * x0 ** (n - k) for k in range(n + 1))

def vietas_dict(deg):
    coeff_symbols = [a, b, c, d, e_coef, f, g, h, i_coef]
    return {eval(f"e{k}"): ((-1) ** k) * coeff_symbols[k] for k in range(deg + 1)}

# ----------------------------------------------------------------------------
#  Derived sums  (unchanged)
# ----------------------------------------------------------------------------
def asum(n):
    return sum(((-1) ** k) * (n - k - 1) * (n - k) * x0 ** (n - k - 2) *
               eval(f"e{k}") for k in range(n - 1))

def bsum(n):
    return sum(((-1) ** k) * k * (n - k) * x0 ** (n - k - 1) *
               eval(f"e{k}") for k in range(1, n))

def csum(n):
    return sum(((-1) ** k) * k * (k - 1) * x0 ** (n - k) *
               eval(f"e{k}") for k in range(2, n + 1))


def polexp_vieta(n):
    """
    Construct the monic polynomial in x0 using e0..e_n with alternating signs:
      sum_{i=0..n} [(-1)^i * e_i * x0^(n-i)].
    Then substitute with the Vieta-like symbols a,b,c,...
    """
    return polexp(n).subs(vietas_dict(n))
# ----------------------------------------------------------------------------
#  One‑shot common_calc(j)  (unchanged)
# ----------------------------------------------------------------------------
def common_calc(j):
    """
    Runs the core logic:
    - Constructs the monic polynomial (polexp) for degree j, setting e0=1.
    - Builds the formula (bsum^2 - asum*csum)/(j-1)^2 and collects terms in x0.
    - For j >= 4, subtracts multiples of the polynomial from the formula.
    - Returns the final list of terms, called 'fixed'.
    """
    # Step 1: The polynomial
    polyno = polexp(j).subs({e0: 1})

    # Step 2: The derived formula
    formula = (bsum(j) ** 2 - asum(j) * csum(j)) / (j - 1) ** 2

    # Step 3: Collect in powers of x0, set e0=1
    grouped_formula = formula.collect(x0).subs({e0: 1})

    # Break it into terms that contain x0 and those that do not
    new1 = grouped_formula.operands()
    lonely_terms = [t for t in new1 if not t.has(x0)]
    fixed = [t for t in new1 if t not in lonely_terms] + [sum(lonely_terms)]
    leading = fixed[0].subs({x0: 1})

    # Step 4: Subtraction of polynomial multiples if j >= 4
    if j >= 4:
        diff = grouped_formula
        for q in range(j - 3):
            # Subtract leading * polyno * x0^(some exponent)
            subi = leading * (polyno * x0 ** (j - 4 - q)).collect(x0).simplify()
            diff = (diff - subi).collect(x0).simplify()
            new1 = diff.operands()
            lonely_terms = [t for t in new1 if not t.has(x0)]
            fixed = [t for t in new1 if t not in lonely_terms] + [sum(lonely_terms)]
            leading = fixed[0].subs({x0: 1})

    # Final fix in case of any leftover changes
    lonely_terms = [t for t in new1 if not t.has(x0)]
    fixed = [t.subs({x0:1}) for t in new1 if t not in lonely_terms] + [sum(lonely_terms)]

    return fixed

# ----------------------------------------------------------------------------
#  Convenience wrappers  (unchanged)
# ----------------------------------------------------------------------------
def calc_fixed(j):
    return common_calc(j)

def calc_vieta_sum(j):
    return [t.subs(vietas_dict(j)) for t in common_calc(j)]

def calc_rootis(j):
    return [t.subs({x0: 1}).subs(ele_dict(j)).simplify().factor()
            for t in common_calc(j)]

# ----------------------------------------------------------------------------
#  NEW – iterate down to an arbitrary target degree
# ----------------------------------------------------------------------------
def iterate_common_calc_to_degree(j, target_deg=2, *, return_all=False,
                                  var_name="T"):
    """
    Repeatedly apply common_calc until the current degree equals target_deg.

    Parameters
    ----------
    j : int
        Starting degree (j ≥ target_deg ≥ 2).
    target_deg : int, default 2
        The degree at which to stop the cascade.
    return_all : bool, default False
        If True, also return every intermediate coefficient list.
    var_name : str, default "T"
        Symbol used in the final monic polynomial.

    Returns
    -------
    final_poly : monic polynomial of degree = target_deg
    history    : list[list] (only when return_all=True)
    """
    if not (isinstance(j, int) and isinstance(target_deg, int)):
        raise TypeError("degrees must be integers")
    if j < target_deg or target_deg < 2:
        raise ValueError("require j ≥ target_deg ≥ 2")

    curr_deg  = j
    coeffs    = None
    history   = []

    while curr_deg > target_deg:
        terms = common_calc(curr_deg)
        print(terms)

        if coeffs is not None:
            subst = {eval(f"e{k}"): (-1) ** k * coeffs[k - 1]
                     for k in range(1, curr_deg + 1)}
            subst[eval("e0")] = 1
            terms = [t.subs(subst).simplify() for t in terms]

        coeffs  = terms[:curr_deg]   # first curr_deg items are the new coeffs
        history.append(coeffs)
        curr_deg -= 1

    # build the final monic polynomial of degree target_deg
    V = SR.var(var_name)
    poly = 0
    print(coeffs)
    for k, ck in enumerate(coeffs, start=0):
        poly += ck * V ** (target_deg - k)
    return (poly, history) if return_all else poly

# ----------------------------------------------------------------------------
#  Thin convenience shims (keep the old “quadratic” name for backward compat)
# ----------------------------------------------------------------------------
def cascade_fixed(j, *, to_deg=2):
    return iterate_common_calc_to_degree(j, to_deg)

def cascade_vieta_sum(j, *, to_deg=2):
    return cascade_fixed(j, to_deg=to_deg).subs(vietas_dict(j))

def cascade_rootis(j, *, to_deg=2):
    return cascade_fixed(j, to_deg=to_deg).subs(ele_dict(j)).simplify().factor()

# ----------------------------------------------------------------------------
#  Optional self‑test  (commented out)
# ----------------------------------------------------------------------------
# if __name__ == "__main__":
#     poly, trail = iterate_common_calc_to_degree(6, 3, return_all=True)
#     print("Final cubic :", poly)
#     print("History len :", len(trail))
