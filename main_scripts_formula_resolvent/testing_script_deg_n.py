from functions_resolvent_calculation import calc_fixed, calc_vieta_sum,calc_rootis, calc_rootis_original, polexp, polexp_vieta
from sage.all import *
var_list = ["x" + str(i) for i in range(100)] + ["e" + str(i) for i in range(100)]
var(var_list + ["n", "x", "T"])
var("a b c d e_coef f g h i_coef")

j = 6
print("Polynomial =", polexp(j))
print("Polynomial =", polexp_vieta(j))
print("Fixed terms =", calc_fixed(j))
print("Vieta sum =", calc_vieta_sum(j))
for k in range(3,7):
    print("Root expansions =", calc_rootis(k)[0].factor())

