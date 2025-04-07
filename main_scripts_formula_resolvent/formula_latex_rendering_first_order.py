from sage.all import *

# Declare variables for the x's and e's.
var_list = ["x" + str(i) for i in range(100)] + ["e" + str(i) for i in range(100)]
var(var_list + ["n"])

# Declare symbolic coefficients for the monic polynomial.
# (We use i_coef for the 9th coefficient to avoid conflict with the imaginary unit.)
var('a b c d e_coef f g h i_coef')

# Define the symmetric functions object for elementary symmetric functions.
E = SymmetricFunctions(QQ).e()  # Using E to avoid clashing with the symbolic e's.

def ele_dict(deg):
    """
    Returns a dictionary mapping the elementary symmetric variables
    e0, e1, ..., e_deg to their expressions in terms of the x's.
    """
    es = [E[i].expand(deg) for i in range(deg + 1)]
    coe = [globals()["e"+str(i)] for i in range(deg + 1)]
    return dict(zip(coe, es))

def vietas_dict(deg):
    """
    Returns a dictionary mapping the elementary symmetric variables e0, e1, ..., e_deg
    to their values via Vieta's formulas for a monic polynomial.
    
    For a monic polynomial, we have:
      e₀ = 1,
      e₁ = –a,
      e₂ = b,
      e₃ = –c,
      e₄ = d,
      e₅ = –e_coef,
      e₆ = f,
      e₇ = –g,
      e₈ = h,
      e₉ = –i_coef,
      ...
    """
    coeff_symbols = [a, b, c, d, e_coef, f, g, h, i_coef]
    subs_dict = {}
    for k in range(deg+1):
        ek = globals()["e"+str(k)]
        #if k == 0:
        #    subs_dict[ek] = 1
        #else:
        subs_dict[ek] = (-1)**k * coeff_symbols[k]
    return subs_dict

def new_sum(n):
    """
    Computes the sum:
      \sum_{k=0}^{n-1} (-1)^k (n-k) x1^(n-k-1) e_k(X_n)
    """
    return sum(
        (-1)**k * (n - k) * x1**(n - k - 1) * globals()["e"+str(k)]
        for k in range(n)
    )

# Loop over degrees j from 2 to 8.
for j in range(2, 9):
    expr = new_sum(j)
    
    # Group the expression by powers of x1.
    grouped_expr = expr.collect(x1)
    
    # Generate LaTeX code for the grouped expression.
    latex_grouped_expr = latex(grouped_expr)
    
    # Substitute elementary symmetric variables via Vieta's formulas.
    substituted_vieta = expr.subs(vietas_dict(j)).full_simplify().factor().collect(x1)
    
    # Substitute elementary symmetric variables by their expressions in terms of the x's.
    substituted_ele = expr.subs(ele_dict(j)).full_simplify().factor()
    
    print("Degree j =", j)
    print("Grouped expression (by powers of x₁):")
    print(grouped_expr)
    print("\nLaTeX code for grouped expression:")
    print(latex_grouped_expr)
    print("\nAfter substitution using Vieta's formulas:")
    print(substituted_vieta)
    print("\nLaTeX code for substitution using Vieta's formulas:")
    print(latex(substituted_vieta))
    print("\nResults after substitution for elementary symmetric variables:")
    print(substituted_ele)
    print("\n" + "="*50 + "\n")
