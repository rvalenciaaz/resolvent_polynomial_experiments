#!/usr/bin/env sage -python

from sage.all import PolynomialRing, QQ

# 1. Define a polynomial ring in x over Q
R = PolynomialRing(QQ, 'x')
x = R.gen()

print("Checking all cubic polynomials: x^3 + b x^2 + c x + d, with b, c, d in [-5, 5]\n")

count = 0
irreducible_count = 0

# 2. Loop over all combinations of b, c, d
for b in range(-5, 6):
    for c in range(-5, 6):
        for d in range(-5, 6):
            f = x**3 + b*x**2 + c*x + d
            count += 1

            print(f"Polynomial #{count}: f(x) = {f}")

            # 3. Check irreducibility over Q
            if f.is_irreducible():
                irreducible_count += 1
                print("    Irreducible over Q: Yes")

                # 4. Compute Galois group using PARI
                G = f.galois_group(pari_group=True)
                print(f"    Galois group: {G}\n")
            else:
                print("    Irreducible over Q: No")
                print("    Skipping Galois group computation\n")

print(f"Total polynomials checked: {count}")
print(f"Total irreducible polynomials: {irreducible_count}")
