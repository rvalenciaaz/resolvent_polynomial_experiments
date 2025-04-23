from sympy import symbols, expand, I, pi, exp, simplify

# Define variables x0, x1, x2, x3, x4
x = symbols('x0 x1 x2 x3 x4')

# Define 5th root of unity zeta = e^(2πi/5)
zeta = exp(2 * pi * I / 5)

# Compute the product over j = 1 to 4 of the linear forms
product = 1
for j in range(1, 5):
    linear_form = sum(zeta**(j*k) * x[k] for k in range(5))
    product *= linear_form

# Expand the final expression
expanded_product = expand(product)

# Simplify (optional, might be slow or complex)
simplified_product = simplify(expanded_product)

print(simplified_product)
