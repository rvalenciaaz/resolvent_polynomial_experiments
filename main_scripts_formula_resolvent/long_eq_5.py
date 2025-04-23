
from sage.all import *
# Define the variables
var('x b c d e_coef f')

# Define each term of the polynomial
term4 = (b**4 - 5*b**2*c + 4*c**2 + 6*b*d - 15*e_coef)*x**4
term3 = (b**3*c - 4*b*c**2 - b**2*d + 12*c*d - 7*b*e_coef - 25*f)*x**3
term2 = (b**3*d - 4*b*c*d - b**2*e_coef + 9*d**2 + c*e_coef - 15*b*f)*x**2
term1 = (b**3*e_coef - 4*b*c*e_coef - b**2*f + 9*d*e_coef - 5*c*f)*x
term0 = (b**3*f - 4*b*c*f + e_coef**2 + 5*d*f)

# Define the full polynomial
P = term4 + term3 + term2 + term1 + term0

# Solve the equation P == 0 for x
solutions = solve(P == 0, x)

# Display the solutions
for soli in solutions:
    print(soli)
    print("\n")

