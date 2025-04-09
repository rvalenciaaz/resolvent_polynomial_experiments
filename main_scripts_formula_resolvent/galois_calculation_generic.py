#!/usr/bin/env sage -python

from sage.all import PolynomialRing, QQ

# 1. Define a polynomial ring in t
T = PolynomialRing(QQ, 't')
t = T.gen()

# 2. Define a polynomial ring in x over Q[t]
R = PolynomialRing(T, 'x')
x = R.gen()

# 3. Define the Lecacheux family: f_t(x) = x^3 - 3*t*x - (t^3 + 1)
f = x**3 - 3*t*x - (t**3 + 2)

print("Cubic Family: f_t(x) = x^3 - 3 t x - (t^3 + 1)\n")

# 4. Loop over integer values of t
for val in range(-3, 5):
    # Evaluate f at t = val
    coeff_ring = PolynomialRing(QQ, 'x')
    x_ = coeff_ring.gen()
    f_val = f(t=val).change_ring(QQ)
    f_val = coeff_ring(f_val)

    print(f"t = {val:2d}  =>  f_{val}(x) = {f_val}")
    
    # Check irreducibility
    if f_val.is_irreducible():
        print("    Irreducible over Q: Yes")
        G = f_val.galois_group(pari_group=True)
        print(f"    Galois group: {G}\n")
    else:
        print("    Irreducible over Q: No")
        print("    Skipping Galois group computation\n")
