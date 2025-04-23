from sage.all import QuadraticField, PolynomialRing, sqrt, QQ
from functions_resolvent_calculation import calc_rootis

def factor_multivar_over_Qsqrt_neg(j, *, pos=0, clear_denom=True, verbose=True):
    """
    Factor the multivariate minimal‐polynomial of calc_rootis(j)[pos]
    over K = Q(√−j), printing both embeddings s→+√(−j) and s→−√(−j).
    """
    # 1) Get the raw symbolic expression
    raw = calc_rootis(j)[pos].expand()

    # 2) Build K = Q(s) with s^2 = -j
    K.<s> = QuadraticField(-j)
    sqrt_neg_j = sqrt(-j)

    # 3) Substitute √(−j) → s, clear any denominators
    exprK = raw.subs({ sqrt_neg_j: s })
    if clear_denom:
        exprK = exprK.numerator()

    # 4) Figure out which x‑vars actually appear
    sym_vars = [v for v in exprK.variables() if v is not s]
    names    = [str(v) for v in sym_vars]

    # 5) Build the multivariate ring K[x0,…,x_{j-1}] (or however many you have)
    PRK = PolynomialRing(K, names)
    gens = PRK.gens()

    # 6) Substitute each symbolic var → its polynomial‑ring generator
    subs_map = { sym_vars[i] : gens[i] for i in range(len(gens)) }
    poly_in_K = exprK.subs(subs_map)

    # 7) Now coerce into PRK (it's already in the ring, but this wraps it as a poly)
    F = PRK(poly_in_K)

    # 8) Factor once (the “+s” embedding)
    fac_plus = F.factor()

    # 9) Conjugate by s→−s
    #    Each factor is a PRK element, so we can .subs on it
    fac_minus = [ (factor.subs({s:-s}), exp) for factor, exp in fac_plus ]

    if verbose:
        print(f"\n— j = {j}, factoring over  Q(√−{j}):")
        print("   embedding s → +√(−j):", fac_plus)
        print("   embedding s → −√(−j):", fac_minus)

    return fac_plus, fac_minus

# Example run
for j in range(3,7):
    factor_multivar_over_Qsqrt_neg(j)
