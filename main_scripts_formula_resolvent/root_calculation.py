#!/usr/bin/env sage -python

# Import everything we need from Sage
from sage.all import var, solve

# Declare our variables
x, e1, e2, e3 = var('x e1 e2 e3')

# Define the polynomial
f = x**2 \
    - ((e1*e2 - 9*e3)/(e1**2 - 3*e2))*x \
    + ((e2**2 - 3*e1*e3)/(e1**2 - 3*e2))

# Solve the equation f(x) == 0
solution = solve(f == 0, x)

# Print the solutions
print("Solutions for x:")
for sol in solution:
    print(sol)
