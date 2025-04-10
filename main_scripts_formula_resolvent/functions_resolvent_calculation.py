#!/usr/bin/env python3

from sage.all import *

# Declare the necessary variables.
var_list = ["x" + str(i) for i in range(100)] + ["e" + str(i) for i in range(100)]
var(var_list + ["n", "x", "T"])
var("a b c d e_coef f g h i_coef")

# Elementary symmetric function generator
_e = SymmetricFunctions(QQ).e()

def ele_dict(deg):
    """
    Map e_i to the expanded elementary symmetric polynomials in x0..x(deg-1).
    Returns a dict {e_i: expanded polynomial in x0, x1, ...}
    """
    return {
        eval("e" + str(i)): _e[i].expand(deg)
        for i in range(deg + 1)
    }

def polexp(n):
    """
    Construct the monic polynomial in x0 using e0..e_n with alternating signs:
      sum_{i=0..n} [(-1)^i * e_i * x0^(n-i)].
    """
    return sum(
        ((-1) ** i) * eval("e" + str(i)) * x0 ** (n - i)
        for i in range(n + 1)
    )

def vietas_dict(deg):
    """
    Map e_k to symbolic coefficients (a, b, c, ...) with alternating signs
    to mimic Vieta's for a monic polynomial.
    """
    coeff_symbols = [a, b, c, d, e_coef, f, g, h, i_coef]
    return {
        globals()["e" + str(k)]: ((-1) ** k) * coeff_symbols[k]
        for k in range(deg + 1)
    }
def polexp_vieta(n):
    """
    Construct the monic polynomial in x0 using e0..e_n with alternating signs:
      sum_{i=0..n} [(-1)^i * e_i * x0^(n-i)].
    """
    return polexp(n).subs(vietas_dict(n))
# Functions for the sums used in the formula
def asum(n):
    """Sum for 'a' in the derived formula."""
    return sum(
        ((-1) ** k) * (n - k - 1) * (n - k) * x0 ** (n - k - 2) * globals()["e" + str(k)]
        for k in range(n - 1)
    )

def bsum(n):
    """Sum for 'b' in the derived formula."""
    return sum(
        ((-1) ** k) * k * (n - k) * x0 ** (n - k - 1) * globals()["e" + str(k)]
        for k in range(1, n)
    )

def csum(n):
    """Sum for 'c' in the derived formula."""
    return sum(
        ((-1) ** k) * k * (k - 1) * x0 ** (n - k) * globals()["e" + str(k)]
        for k in range(2, n + 1)
    )

def common_calc(j):
    """
    Runs the core logic:
    - Constructs the monic polynomial (polexp) for degree j, setting e0=1.
    - Builds the formula (bsum^2 - asum*csum)/(j-1)^2 and collects terms in x0.
    - For j >= 4, subtracts multiples of the polynomial from the formula.
    - Returns the final list of terms, called 'fixed'.

    Called internally by the other functions to avoid code duplication.
    """
    # Step 1: The polynomial
    polyno = polexp(j).subs({e0: 1})

    # Step 2: The derived formula
    formula = (bsum(j) ** 2 - asum(j) * csum(j)) / (j - 1) ** 2

    # Step 3: Collect and set e0=1
    grouped_formula = formula.collect(x0).subs({e0: 1})

    # Identify terms that do not contain x0
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

    # Return the final "fixed" list of terms
    return fixed


def calc_fixed(j):
    """
    Returns the final list of terms ('fixed') for a given j,
    after subtracting multiples of the original polynomial (when j >= 4).
    """
    return common_calc(j)


def calc_vieta_sum(j):
    """
    Returns the 'fixed' terms with Vieta's substitutions (a, b, c, etc.)
    for a given j.
    """
    fixed_terms = common_calc(j)
    return [term.subs(vietas_dict(j)) for term in fixed_terms]


def calc_rootis(j):
    """
    Returns the 'fixed' terms with the elementary‐symmetric expansions
    (i.e., substituting e_i with the expansions in x0..x(j-1)).
    """
    fixed_terms = common_calc(j)
    return [
        term.subs({x0: 1}).subs(ele_dict(j)).simplify().factor()
        for term in fixed_terms
    ]

def common_calc_original(j):
    """
    Runs the core logic:
    - Constructs the monic polynomial (polexp) for degree j, setting e0=1.
    - Builds the formula (bsum^2 - asum*csum)/(j-1)^2 and collects terms in x0.
    - For j >= 4, subtracts multiples of the polynomial from the formula.
    - Returns the final list of terms, called 'fixed'.

    Called internally by the other functions to avoid code duplication.
    """
    # Step 1: The polynomial
    polyno = polexp(j).subs({e0: 1})

    # Step 2: The derived formula
    formula = (bsum(j) ** 2 - asum(j) * csum(j)) / (j - 1) ** 2

    # Step 3: Collect and set e0=1
    grouped_formula = formula.collect(x0).subs({e0: 1})

    # Identify terms that do not contain x0
    new1 = grouped_formula.operands()
    lonely_terms = [t for t in new1 if not t.has(x0)]
    fixed = [t.subs({x0:1}) for t in new1 if t not in lonely_terms] + [sum(lonely_terms)]
    #leading = fixed[0].subs({x0: 1})
    '''
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
    '''
    # Return the final "fixed" list of terms
    return fixed

def calc_vieta_sum_original(j):
    """
    Returns the 'fixed' terms with Vieta's substitutions (a, b, c, etc.)
    for a given j.
    """
    fixed_terms = common_calc_original(j)
    return [term.subs(vietas_dict(j)) for term in fixed_terms]
# If you want to do a quick test inside this script, you can uncomment below:
# if __name__ == "__main__":
#     j_test = 4
#     print("calc_fixed:", calc_fixed(j_test))
#     print("calc_vieta_sum:", calc_vieta_sum(j_test))
#     print("calc_rootis:", calc_rootis(j_test))
