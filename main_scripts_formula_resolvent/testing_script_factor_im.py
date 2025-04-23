from functions_resolvent_cascade import calc_fixed, calc_vieta_sum, calc_rootis, polexp, polexp_vieta
from sage.all import *

# Declare necessary variables
var_list = ["x" + str(i) for i in range(100)] + ["e" + str(i) for i in range(100)]
var(var_list + ["n", "x", "T"])
var("a b c d e_coef f g h i_coef")

def factor_over_quadratic_field(j):
    """
    Computes the root expression for the given j, and factors it over Q(sqrt(-j)).
    """
    # Step 1: Compute the root expression
    root_expr = calc_rootis(j)[0]
    print(f"Root expansion for j={j}:", root_expr)

    # Step 2: Define the quadratic field Q(sqrt(-j))
    K = QuadraticField(-j, 's')
    s = K.gen()  # This is sqrt(-j)

    # Step 3: Coerce expression into that field
    # Note: Ensure root_expr is a polynomial in SR
    expr_in_K = SR(root_expr).change_ring(K)

    # Step 4: Factor in the extended field
    factored = expr_in_K.factor()
    print(f"Factorization over Q(sqrt(-{j})):", factored)

    return factored

# Example usage:
j = 4
factor_over_quadratic_field(j)
