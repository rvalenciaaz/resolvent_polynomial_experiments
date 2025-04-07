########################
# Sympy version of code
########################

import itertools
from sympy import (
    symbols, Symbol, exp, pi, I, simplify, factor, collect, latex,
    Add, Pow, Mul, prod
)

#
# 1) Declare our main symbols:
#
# We want x0,...,x99 and e0,...,e99, plus n and x.
#
x_vars = [Symbol(f"x{i}", complex=True) for i in range(100)]
e_vars = [Symbol(f"e{i}", complex=True) for i in range(100)]
n, x = symbols('n x', complex=True)

#
# 2) Declare symbolic coefficients for the original polynomial.
#    Also note that we need a 9th coefficient "i_" (instead of "i")
#    so as not to conflict with Sympy's imaginary unit "I".
#
a, b, c, d, e_coef, f_, g, h, i_ = symbols('a b c d e_coef f g h i_', complex=True)

#
# 3) Elementary symmetric polynomials in Sympy:
#    For i-th E.S.P. in variables [x0, x1, ..., x_{deg-1}],
#    we sum all products of i distinct x’s.
#
def elementary_symmetric_poly(i, vars_list):
    """
    Returns the i-th elementary symmetric polynomial in the given list of variables.
    e.g. for i=2 and vars_list=[x0,x1,x2], returns x0*x1 + x0*x2 + x1*x2.
    """
    if i == 0:
        return 1
    result = 0
    for combo in itertools.combinations(vars_list, i):
        result += prod(combo)  # Sympy's product of elements in 'combo'
    return result

#
# 4) Build the dictionary e0->(sum of x's^0), e1->(sum of x's^1), etc.
#    This mimics the Sage approach "SymmetricFunctions(QQ).e()[i].expand(deg)".
#
def ele_dict(deg):
    """
    Returns a dict that maps e0, e1, ..., e_deg  to their expansions in x0..x_{deg-1}.
    e0 = 1
    e1 = x0 + ... + x_{deg-1}
    e2 = sum of all x_i*x_j for i<j
    ...
    """
    es_expressions = [elementary_symmetric_poly(i, x_vars[:deg]) for i in range(deg+1)]
    return dict(zip(e_vars[:deg+1], es_expressions))

#
# 5) Define a function to map x0->zeta^0, x1->zeta^1, etc., where zeta = exp(2*pi*I/deg).
#
def root_unity(deg):
    """
    Return a dict with variables x0,...,x_{deg-1} as keys
    and the corresponding powers of the deg-th root of unity as values.
    """
    zeta = exp(2*pi*I/deg)
    roots_dict = {}
    for expo, x_sym in enumerate(x_vars[:deg]):
        roots_dict[x_sym] = zeta**expo
    return roots_dict

#
# 6) Define the "polexp(n)" which sums up  (-1)^i * e_i * x0^(n - i).
#
def polexp(n):
    return sum(
        ((-1)**i)*e_vars[i]*(x_vars[0]**(n-i))
        for i in range(n+1)
    )

#
# 7) Vieta's-like dictionary mapping e0,...,e_deg to +/- the polynomial coefficients.
#    e0 => (-1)^0*a0, e1 => (-1)^1*a1, etc.
#
def vietas_dict(deg):
    """
    Returns a dictionary for e0, e1, ..., e_deg:
       e_k -> (-1)^k * [k-th entry of (a, b, c, d, e_coef, f_, g, h, i_)]
    Up to the index deg.
    """
    # We store a, b, c, d, e_coef, f_, g, h, i_
    coeff_list = [a, b, c, d, e_coef, f_, g, h, i_]
    subs_dict = {}
    for k in range(deg+1):
        subs_dict[e_vars[k]] = ((-1)**k)*coeff_list[k]
    return subs_dict

#
# 8) Sums used in the formula: asum, bsum, csum.
#    Each uses x0, e0, e1, ... e_n in the pattern from the Sage code.
#
def asum(n):
    # sum_{k=0..n-1} [ (-1)^k * (n-k-1)*(n-k)* x0^(n-k-2)* e_k ]
    return sum(
        ((-1)**k) * (n - k - 1) * (n - k) * (x_vars[0]**(n - k - 2)) * e_vars[k]
        for k in range(n-1)
    )

def bsum(n):
    # sum_{k=1..n-1} [ (-1)^k * k*(n-k) * x0^(n-k-1) * e_k ]
    return sum(
        ((-1)**k) * k * (n - k) * (x_vars[0]**(n - k - 1)) * e_vars[k]
        for k in range(1, n)
    )

def csum(n):
    # sum_{k=2..n} [ (-1)^k * k*(k-1) * x0^(n-k) * e_k ]
    return sum(
        ((-1)**k) * (k * (k - 1)) * (x_vars[0]**(n - k)) * e_vars[k]
        for k in range(2, n+1)
    )

#
# Main loop: j from 3 to 5, as in the Sage code.
#
for j in range(3, 6):

    # Build the polynomial by substituting e0 = 1 into polexp(j).
    polyno = polexp(j).subs({e_vars[0]: 1})

    # The formula = (bsum(j)^2 - asum(j)*csum(j)) / (j-1)^2
    formula = (bsum(j)**2 - asum(j)*csum(j)) / (j-1)**2

    # Group by powers of x0, then also set e0->1
    grouped_formula = collect(formula, x_vars[0]).subs({e_vars[0]:1})

    # Get latex representation of that grouped formula
    latex_grouped_formula = latex(grouped_formula)

    # Substitute the elementary symmetric variables with Vieta's dictionary
    # and factor/simplify:
    substituted = formula.subs(vietas_dict(j)).simplify().factor()
    grouped_subs = collect(substituted, x_vars[0]).subs({a:1})

    # Also substitute e0,e1,... with expansions in x0,... x_{j-1}:
    subs_ele = formula.subs(ele_dict(j)).simplify().factor()

    # The next part of the code tries to mimic the Sage .operands() approach:
    # We'll treat the expression as a sum of terms: new1 = expression.as_ordered_terms().
    # Then do the same logic for 'lonely_terms', 'fixed', etc.
    new1 = collect(grouped_formula, x_vars[0]).as_ordered_terms()
    lonely_terms = [term for term in new1 if not term.has(x_vars[0])]
    fixed = [term for term in new1 if term not in lonely_terms] + [sum(lonely_terms)]
    leading = fixed[0].subs({x_vars[0]:1})

    # If j==4, they do a certain difference-based logic, else if j>4, another logic, else j<4...
    # We'll just replicate that flow:
    if j == 4:
        diff = grouped_formula - leading*polyno
        diff_sim = collect(diff.simplify(), x_vars[0])
        new1 = diff_sim.as_ordered_terms()

    elif j > 4:
        diff = grouped_formula
        for cou in range(0, j-3):
            subi = collect(leading * polyno * (x_vars[0]**(j-4-cou)), x_vars[0]).simplify()
            diff = collect(diff - subi, x_vars[0]).simplify()
            new1 = diff.as_ordered_terms()
            lonely_terms = [term for term in new1 if not term.has(x_vars[0])]
            fixed = [term for term in new1 if term not in lonely_terms] + [sum(lonely_terms)]
            leading = fixed[0].subs({x_vars[0]:1})
            new1 = diff.as_ordered_terms()
    else:
        # j<4 (that is j=3), they basically do no special difference logic
        pass

    lonely_terms = [term for term in new1 if not term.has(x_vars[0])]
    fixed = [term for term in new1 if term not in lonely_terms] + [sum(lonely_terms)]
    leading = fixed[0].subs({x_vars[0]:1})
    div_leading = [val / leading for val in fixed]

    # Print out results to mimic the Sage prints
    print("Degree j =", j)
    print("\nPolynomial:")
    print(polyno)
    print("\nGrouped formula (by powers of x0):")
    print(grouped_formula)
    print("\nLaTeX code for grouped formula:")
    print(latex_grouped_formula)
    print("\nAfter substitution using Vieta's formulas (and setting a=1 in the result):")
    print(grouped_subs)
    print("\nLaTeX code for the above Vieta-substituted expression:")
    print(latex(grouped_subs))
    print("\nResults after direct substitution for e_k in terms of x0..x_{j-1}:")
    print(subs_ele)

    print("\nSubtraction steps / 'fixed' list:")
    print(fixed)
    print("\nSum of fixed terms, collected in x0, after Vieta substitution:")
    print(collect(sum(fixed).subs(vietas_dict(j)), x_vars[0]))

    print("\nSum of the fixed terms divided by leading, substituted in Vieta, then x0->x:")
    print(
        collect(
            sum(div_leading).subs(vietas_dict(j)).subs({x_vars[0]: x}),
            x
        )
    )

    print("\nSum of the fixed terms divided by leading, but ignoring Vieta, with x0->x:")
    print(
        collect(
            sum(div_leading).subs({x_vars[0]: x}),
            x
        )
    )
    print("\nLeading term:")
    print(leading)
    print("\nLeading term after substituting e_k expansions (and simplifying):")
    lea_roots = simplify(factor(leading.subs(ele_dict(j))))
    print(lea_roots)
    print("\nLeading term after also substituting x_k -> deg-th roots of unity:")
    lea_uni = simplify(factor(lea_roots.subs(root_unity(j))))
    print(lea_uni)
    print("\n" + "="*50 + "\n")
