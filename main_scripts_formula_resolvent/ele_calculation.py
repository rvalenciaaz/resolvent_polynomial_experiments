#!/usr/bin/env sage -python

# Import everything we need from Sage
from sage.all import *

e = SymmetricFunctions(QQ).e()

def ele_dict(deg):
    es = [e[i].expand(deg) for i in range(deg + 1)]
    coe = [eval("e" + str(i)) for i in range(deg + 1)]
    return dict(zip(coe, es))

# Declare our variables
x, e0, e1, e2, e3, e4 = var('x e0 e1 e2 e3 e4')

# Define the polynomial
#f = x**3 - (e1**2*e2 - 4*e2**2 + 2*e1*e3 + 16*e4)*x**2/(e1**3 - 4*e1*e2 + 8*e3) + (e1**2*e3 - 4*e2*e3 + 8*e1*e4)*x/(e1**3 - 4*e1*e2 + 8*e3) - (e1**2*e4 - e3**2)/(e1**3 - 4*e1*e2 + 8*e3) 

expr1=(e1**2*e2 - 4*e2**2 + 2*e1*e3 + 16*e4)/(e1**3 - 4*e1*e2 + 8*e3)
print(expr1.subs(ele_dict(4)).simplify().factor())
