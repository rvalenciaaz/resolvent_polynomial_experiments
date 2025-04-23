from functions_resolvent_cascade import calc_fixed, calc_vieta_sum, calc_rootis, polexp, polexp_vieta
from sage.all import *

# Declare symbolic variables
var_list = ["x" + str(i) for i in range(100)] + ["e" + str(i) for i in range(100)]
var(var_list + ["n", "x", "T"])
var("a b c d e_coef f g h i_coef")

def factor_over_quadratic_field(j):
    """
    Compute and factor root expression over Q(sqrt(-j)) using PolynomialRing instead of symbolic expressions.
    """
    # Step 1: Get the root expression (symbolic)
    root_expr = calc_rootis(j)[0]
    print(f"Root expansion for j={j}:", root_expr)

    # Step 2: Define quadratic field Q(sqrt(-j))
    K = QuadraticField(-j, 's')
    s = K.gen()

    # Step 3: Identify variables in expression
    vars_in_expr = list(root_expr.variables())

    # Step 4: Create multivariate polynomial ring over K
    P = PolynomialRing(K, names=[str(v) for v in vars_in_expr])
    var_map = {SR(v): P.gen(i) for i, v in enumerate(vars_in_expr)}

    # Step 5: Convert symbolic expression into a polynomial over K
    poly_expr = root_expr.subs(var_map)
    poly_in_K = P(poly_expr)

    # Step 6: Factor the polynomial
    factored = poly_in_K.factor()
    print(f"Factorization over Q(sqrt(-{j})):", factored)

    return factored

# Example usage
j = 5
factor_over_quadratic_field(j)
