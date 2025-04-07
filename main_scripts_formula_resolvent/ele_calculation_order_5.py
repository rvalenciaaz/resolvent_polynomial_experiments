#!/usr/bin/env sage -python

# Import everything we need from Sage
from sage.all import *

e = SymmetricFunctions(QQ).e()

def ele_dict(deg):
    es = [e[i].expand(deg) for i in range(deg + 1)]
    coe = [eval("e" + str(i)) for i in range(deg + 1)]
    return dict(zip(coe, es))

# Declare our variables
x, e0, e1, e2, e3, e4, e5 = var('x e0 e1 e2 e3 e4 e5')

print(ele_dict(5))
# Define the polynomial

expr1=e1**4 - 5*e1**2*e2 + 4*e2**2 + 6*e1*e3 - 15*e4
print(expr1.subs(ele_dict(5)).simplify().factor())
