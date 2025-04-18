#!/usr/bin/env sage -python
# -*- coding: utf-8 -*-

from sage.all import *

###############################################################################
# Step 1: Define polynomial ring S in b, c, d, e_coef over QQ
###############################################################################
S = PolynomialRing(QQ, ['b','c','d'])
b, c, d = S.gens()  # Extract the ring generators

###############################################################################
# Step 2: Define the field of rational functions in (b,c,d,e_coef)
###############################################################################
K = S.fraction_field()

###############################################################################
# Step 3: Define a univariate polynomial ring R in x over K
###############################################################################
R = PolynomialRing(K, 'x')  # No shorthand: R.<x> = ...
x = R.gen()

###############################################################################
# Step 4: Define the denominator and polynomial coefficients
###############################################################################
D = (b**2 - 3*c)

coef_x1 = (b*c - 9*d) / D
coef_x0 = (c**2 - 3*b*d) / D

###############################################################################
# Step 5: Construct the polynomial P(x)
###############################################################################
P = x**2 + coef_x1*x + coef_x0

###############################################################################
# Step 6: Compute the discriminant
###############################################################################
disc = P.discriminant()

###############################################################################
# Step 7: Print the results
###############################################################################
print("Polynomial P(x) =", P)
print("Discriminant =", disc)
