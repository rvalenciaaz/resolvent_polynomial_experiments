from functions_resolvent_calculation import calc_fixed, calc_vieta_sum, calc_rootis, polexp, polexp_vieta
from sage.all import *
var_list = ["x" + str(i) for i in range(100)] + ["e" + str(i) for i in range(100)]
var(var_list + ["n", "x", "T"])
var("a b c d e_coef f g h i_coef")

j = 4
print("Polynomial =", polexp(j))
print("Polynomial =", polexp_vieta(j))
print("Fixed terms =", calc_fixed(j))
print("Vieta sum =", calc_vieta_sum(j))
print("Root expansions =", calc_rootis(j))

print("\n Replaced by C4 \n")
vieta_sum=calc_vieta_sum(j)
repi = [expr.subs({b: 7, c: -6, d: -2, e_coef: 1}).simplify().factor().subs({x0: 1}) for expr in vieta_sum]
disco=(repi[1]**2-4*repi[0]*repi[1]).full_simplify().factor()
for ico, termo in enumerate(repi):
    print("\n", ico, " term/coefficient:")
    print(termo, "\n")
print("\n", "Discriminant", "\n", disco, "\n")

print("\n Replaced by C4 \n")
vieta_sum=calc_vieta_sum(j)
repi = [expr.subs({b: 6, c: 1 , d: -4, e_coef: 1}).simplify().factor().subs({x0: 1}) for expr in vieta_sum]
disco=(repi[1]**2-4*repi[0]*repi[1]).full_simplify().factor()
for ico, termo in enumerate(repi):
    print("\n", ico, " term/coefficient:")
    print(termo, "\n")
print("\n", "Discriminant", "\n", disco, "\n")

print("\n Replaced by simplest quartic \n")
vieta_sum=calc_vieta_sum(j)
repi = [expr.subs({b: -T, c: -6, d: T, e_coef: 1}).simplify().factor().subs({x0: 1}) for expr in vieta_sum] 
disco=(repi[1]**2-4*repi[0]*repi[1]).full_simplify().factor()
for ico, termo in enumerate(repi):
    print("\n", ico, " term/coefficient:")
    print(termo, "\n")
print("\n", "Discriminant", "\n", disco, "\n")

print("\n Replaced by simplest quartic \n")
vieta_sum=calc_vieta_sum(j)
repi = [expr.subs({b: 4, c: -3, d: -14, e_coef: 1}).simplify().factor().subs({x0: 1}) for expr in vieta_sum]
disco=(repi[1]**2-4*repi[0]*repi[1]).full_simplify().factor()
for ico, termo in enumerate(repi):
    print("\n", ico, " term/coefficient:")
    print(termo, "\n")
print("\n", "Discriminant", "\n", disco, "\n")
