from sage.all import *

# Declare variables
var_list = ["x" + str(i) for i in range(100)] + ["e" + str(i) for i in range(100)]
var(var_list + ["n", "x", "T"])
var("a b c d e_coef f g h i_coef")

# Elementary symmetric functions placeholder
e = SymmetricFunctions(QQ).e()

def ele_dict(deg):
    """Map e_i to the expanded elementary symmetric polynomials in x0..x(deg-1)."""
    return dict(
        zip(
            [eval("e" + str(i)) for i in range(deg + 1)],
            [e[i].expand(deg) for i in range(deg + 1)]
        )
    )

def root_unity(deg):
    """Return a dict x_k -> n-th roots of unity."""
    zeta = exp(2 * pi * I / deg)
    return {
        eval("x" + str(k)): zeta**k for k in range(deg)
    }

def polexp(n):
    """Construct the monic polynomial from e0..e_n in x0 with alternating signs."""
    return sum(
        ((-1) ** i) * eval("e" + str(i)) * x0 ** (n - i)
        for i in range(n + 1)
    )

def vietas_dict(deg):
    """
    Map e_k to coefficient symbols (a, b, c, ...) with alternating signs 
    to mimic Vieta's for a monic polynomial.
    """
    coeff_symbols = [a, b, c, d, e_coef, f, g, h, i_coef]
    return {
        globals()["e" + str(k)]: ((-1) ** k) * coeff_symbols[k]
        for k in range(deg + 1)
    }

def asum(n):
    """Sum for 'a' in the formula."""
    return sum(
        ((-1) ** k) * (n - k - 1) * (n - k) * x0 ** (n - k - 2) * globals()["e" + str(k)]
        for k in range(n - 1)
    )

def bsum(n):
    """Sum for 'b' in the formula."""
    return sum(
        ((-1) ** k) * k * (n - k) * x0 ** (n - k - 1) * globals()["e" + str(k)]
        for k in range(1, n)
    )

def csum(n):
    """Sum for 'c' in the formula."""
    return sum(
        ((-1) ** k) * k * (k - 1) * x0 ** (n - k) * globals()["e" + str(k)]
        for k in range(2, n + 1)
    )

# Main loop
for j in range(3, 6):
    # The polynomial
    polyno = polexp(j).subs({e0: 1})

    # Formula from sums
    formula = (bsum(j) ** 2 - asum(j) * csum(j)) / (j - 1) ** 2

    # Collect terms in x0 and force e0=1
    grouped_formula = formula.collect(x0).subs({e0: 1})

    # Split out terms that don't involve x0
    new1 = grouped_formula.operands()
    lonely_terms = [term for term in new1 if not term.has(x0)]
    fixed = [term for term in new1 if term not in lonely_terms] + [sum(lonely_terms)]
    leading = fixed[0].subs({x0: 1})

    # Subtract out multiples of the original polynomial if j >= 4
    if j >= 4:
        diff = grouped_formula
        for cou in range(j - 3):
            subi = leading * (polyno * x0 ** (j - 4 - cou)).collect(x0).simplify()
            diff = (diff - subi).collect(x0).simplify()
            new1 = diff.operands()
            lonely_terms = [term for term in new1 if not term.has(x0)]
            fixed = [term for term in new1 if term not in lonely_terms] + [sum(lonely_terms)]
            leading = fixed[0].subs({x0: 1})

    # Re-collect final pieces
    lonely_terms = [term for term in new1 if not term.has(x0)]
    fixed = [term for term in new1 if term not in lonely_terms] + [sum(lonely_terms)]

    # Print general info
    print("Degree j =", j)
    print("\nPolynomial")
    print(polyno)
    print("\nPolynomial coefficients")
    print(polyno.subs(vietas_dict(j)))

    print("\n Substracting the original polynomial\n")
    print(fixed)
    print("\n")

    # Substitute with Vieta's dict
    vieta_sum = [u.subs(vietas_dict(j)) for u in fixed]
    print(vieta_sum)

    # Specific replacements for j=3,4,5
    if j == 3:
        print("\n Replaced \n")
        repi = [
            expr.subs({b: -(T**3 - 2*T**2 + 3*T - 3), c: -T**2, d: -1})
                .simplify().factor().subs({x0: 1})
            for expr in vieta_sum
        ]
        for ico, termo in enumerate(repi):
            print("\n", ico, " term/coefficient:")
            print(termo, "\n")

    if j == 4:
        print("\n Replaced \n")
        repi = [
            expr.subs({b: -T, c: -6, d: T, e_coef: 1})
                .simplify().factor().subs({x0: 1})
            for expr in vieta_sum
        ]
        for ico, termo in enumerate(repi):
            print("\n", ico, " term/coefficient:")
            print(termo, "\n")

    if j == 5:
        print("\n Replaced \n")
        repi = [
            expr.subs({
                b: T**2,
                c: -(2*T**3 + 6*T**2 + 10*T + 10),
                d: T**4 + 5*T**3 + 11*T**2 + 15*T + 5,
                e_coef: T**3 + 4*T**2 + 10*T + 10,
                f: 1
            }).simplify().factor().subs({x0: 1})
            for expr in vieta_sum
        ]
        for ico, termo in enumerate(repi):
            print("\n", ico, " term/coefficient:")
            print(termo, "\n")

    # Substitute each final term into root variables
    print("\n Coeef to roots")
    rootis = [
        expr.subs({x0: 1}).subs(ele_dict(j)).simplify().factor()
        for expr in fixed
    ]
    print(rootis)
    print("\n" + "=" * 50 + "\n")
