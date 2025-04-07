from sage.all import *

# Declare variables for x's and e's.
var_list = ["x" + str(i) for i in range(100)] + ["e" + str(i) for i in range(100)]
var(var_list + ["n"])

# Declare symbolic coefficients for the original polynomial.
# Note: we rename the coefficient 'e' to 'e_coef' to avoid conflict with the elementary symmetric variables.
var('a b c d e_coef f g h')

# Define the symmetric functions object (renamed to avoid clashing with the symbolic e's).
e = SymmetricFunctions(QQ).e()  # Not used in our final substitutions.

def ele_dict(deg):
    es = [e[i].expand(deg) for i in range(deg + 1)]
    coe = [eval("e" + str(i)) for i in range(deg + 1)]
    return dict(zip(coe, es))

def vietas_dict(deg):
    """
    Returns a dictionary mapping the symbolic variables e0, e1, ..., e_deg
    to their values via Vieta's formulas for a monic polynomial.
    
    For example, for a monic polynomial:
      e0 = 1,
      e1 = -a,
      e2 = b,
      e3 = -c,
      e4 = d,
      e5 = -e_coef,
      e6 = f,
      e7 = -g,
      e8 = h,
      ...
    
    Coefficients are taken in order from the list: [a, b, c, d, e_coef, f, g, h].
    """
    coeff_symbols = [a, b, c, d, e_coef, f, g, h, i]  # Coefficients in order.
    subs_dict = {}
    for k in range(deg+1):
        # Retrieve the symbolic variable e0, e1, ... from the global namespace.
        ek = globals()["e"+str(k)]
        #if k == 0:
        #    subs_dict[ek] = 1
        #else:
        subs_dict[ek] = (-1)**k * coeff_symbols[k]
    return subs_dict

def asum(n):
    return sum(
        (-1)**k * ((n - k - 1) * (n - k) // 2) * x0**(n - k - 2) * globals()["e"+str(k)]
        for k in range(0, n-1)
    )

def bsum(n):
    return sum(
        (-1)**k * k * (n - k) * x0**(n - k - 1) * globals()["e"+str(k)]
        for k in range(1, n)
    )

def csum(n):
    return sum(
        (-1)**k * (k * (k - 1) // 2) * x0**(n - k) * globals()["e"+str(k)]
        for k in range(2, n+1)
    )

for j in range(2, 9):
    formula = (bsum(j)**2 - 4 * asum(j) * csum(j))/(j-1)**2
    
    # Group the expression by powers of x0.
    grouped_formula = formula.collect(x0)
    
    # Generate LaTeX code for the grouped formula.
    latex_grouped_formula = latex(grouped_formula)
    
    # Substitute the elementary symmetric variables with Vieta's formulas.
    substituted = formula.subs(vietas_dict(j)).full_simplify().factor()
    
    grouped_subs= substituted.collect(x0)
    
    subs_ele = formula.subs(ele_dict(j)).full_simplify().factor()
    print("Degree j =", j)
    print("Grouped formula (by powers of x₀):")
    print(grouped_formula)
    print("\nLaTeX code for grouped formula:")
    print(latex_grouped_formula)
    print("\nAfter substitution using Vieta's formulas:")
    print(grouped_subs)
    print("\nLaTeX code for grouped vieta:")
    print(latex(grouped_subs))
    print("\n Results after substitution for roots variables")
    print(subs_ele)
    print("\n" + "="*50 + "\n")
