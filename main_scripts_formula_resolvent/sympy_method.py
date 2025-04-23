from sympy import symbols, expand, factor, I, simplify

# Define symbols
x0, x1, x2, x3 = symbols('x0 x1 x2 x3')

# Define the polynomial
poly = (
    (x0 + x1 - x2 - x3)*(x0 - x1 + x2 - x3)*(x0 - x1 - x2 + x3)
    )

# Try to factor over complex field (allowing i = sqrt(-1))
factored = factor(poly, extension=I)

print(factored)
