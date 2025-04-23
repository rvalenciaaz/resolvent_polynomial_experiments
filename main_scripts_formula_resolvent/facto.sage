# ---------------------------------------------------------------------------
# factor_integer_in_cyclotomic_field.py
# ---------------------------------------------------------------------------
from sage.all import *

def factor_integer_in_cyclotomic(num, n, verbose=True):
    """
    Factor an integer `num` over the cyclotomic field Q(zeta_n),
    where zeta_n is a primitive n-th root of unity.

    Parameters
    ----------
    num : int
        Integer to factor.
    n : int
        Order of the cyclotomic field.
    verbose : bool, optional
        Print intermediate diagnostics if True.

    Returns
    -------
    Factorization
        Factorization of the integer over the cyclotomic field.
    """

    # Define the cyclotomic field Q(zeta_n)
    K.<zeta> = CyclotomicField(n)

    # Factor integer in the cyclotomic field
    factors = K.ideal(num).factor()

    if verbose:
        if len(factors) == 1 and factors[0][1] == 1:
            print(f"{num} is irreducible in ℚ(ζ_{n}).")
        else:
            print(f"Factors of {num} in ℚ(ζ_{n}):")
            for fac, multiplicity in factors:
                print(f"({fac.gens_reduced()[0]})^{multiplicity}")

    return factors


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    factor_integer_in_cyclotomic(59229,19)
