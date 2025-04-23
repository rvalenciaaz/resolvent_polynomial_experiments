# ---------------------------------------------------------------------------
# factor_root_over_Qsqrt_minus_j.py
# ---------------------------------------------------------------------------
from sage.all import *
from functions_resolvent_cascade import calc_rootis        # make sure this is on PYTHONPATH

# (Optional) declare any loose Sage variables that calc_rootis might rely on
var_list = [f"x{i}" for i in range(100)] + [f"e{i}" for i in range(100)]
var(var_list + ["n", "x", "T"])
var("a b c d e_coef f g h i_coef")      # keep these if your module needs them


def factor_over_quadratic_field(j, *, verbose=True, clear_denom=True):
    """
    Factor the minimal polynomial of the first root returned by
    ``calc_rootis(j)`` over the quadratic field Q(sqrt(-j)).

    Parameters
    ----------
    j : int
        Positive integer (the 'j‐invariant' in your context).
    verbose : bool, optional
        Print intermediate diagnostics if True.
    clear_denom : bool, optional
        Clear denominators before coercing into the polynomial ring.

    Returns
    -------
    sage.structure.factorization.Factorization
    """

    # -----------------------------------------------------------------------
    # 1. Obtain the symbolic root expression
    # -----------------------------------------------------------------------
    root_expr = calc_rootis(j)[0].expand()
    if verbose:
        print(f"Root expansion for j = {j}:\n{root_expr}\n")

    # -----------------------------------------------------------------------
    # 2. Define the quadratic field  K = ℚ(√−j)
    # -----------------------------------------------------------------------
    K.<s> = QuadraticField(-j,1)

    # -----------------------------------------------------------------------
    # 3. Replace the stray √(-j) in the expression by the field generator  s
    # -----------------------------------------------------------------------
    sqrt_neg_j = sqrt(-j)                       # the symbolic radical
    root_expr_K = root_expr.subs({sqrt_neg_j: s})

    # -----------------------------------------------------------------------
    # 4. Collect genuine polynomial variables (skip the field generator 's')
    # -----------------------------------------------------------------------
    vars_in_expr = [v for v in root_expr_K.variables() if v is not s]
    if verbose:
        print("Polynomial indeterminates:", vars_in_expr, "\n")

    # -----------------------------------------------------------------------
    # 5. Build a multivariate polynomial ring over K
    # -----------------------------------------------------------------------
    P = PolynomialRing(K, names=[str(v) for v in vars_in_expr])
    var_map = {v: P.gen(i) for i, v in enumerate(vars_in_expr)}

    # -----------------------------------------------------------------------
    # 6. Coerce the expression into that ring
    # -----------------------------------------------------------------------
    coerced = root_expr_K.subs(var_map)
    if clear_denom:
        coerced = coerced.numerator()          # drop any denominators

    poly_in_K = P(coerced)

    if verbose:
        print("Polynomial in K[x₁,…]:", poly_in_K, "\n")

    # -----------------------------------------------------------------------
    # 7. Factor and return
    # -----------------------------------------------------------------------
    factors = poly_in_K.factor()
    if verbose:
        print(f"Factorisation over ℚ(√−{j}):\n{factors}\n")

    return factors


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    j = 3
    factor_over_quadratic_field(j)
