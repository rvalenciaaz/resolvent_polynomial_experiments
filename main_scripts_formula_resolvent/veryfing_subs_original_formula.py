from sage.all import *

var_list = ["x" + str(i) for i in range(100)] + ["e" + str(i) for i in range(100)]
var(var_list + ["n"])
e = SymmetricFunctions(QQ).e()

def ele_dict(deg):
    es = [e[i].expand(deg) for i in range(deg + 1)]
    coe = [eval("e" + str(i)) for i in range(deg + 1)]
    return dict(zip(coe, es))

def asum(n):
    # k runs from 0 to n-2
    return sum(
        (-1)**k * ((n - k - 1) * (n - k) // 2) * x0**(n - k - 2) * eval("e" + str(k))
        for k in range(0, n - 1)
    )

def bsum(n):
    # k runs from 1 to n-1
    return sum(
        (-1)**k * k * (n - k) * x0**(n - k - 1) * eval("e" + str(k))
        for k in range(1, n)
    )

def csum(n):
    # k runs from 2 to n
    return sum(
        (-1)**k * (k * (k - 1) // 2) * x0**(n - k) * eval("e" + str(k))
        for k in range(2, n + 1)
    )

for j in range(2, 9):
    formula = bsum(j)**2 - 4 * asum(j) * csum(j)
    # Group the original expression by powers of x0 (without substitution)
    grouped_formula = formula.collect(x0)
    # Then perform the substitution and simplify/factor
    substituted = formula.subs(ele_dict(j)).full_simplify().factor()
    print("Degree j =", j)
    print("Original formula (grouped by powers of x0):")
    print(grouped_formula)
    print("After substitution:")
    print(substituted)
    print("\n" + "="*50 + "\n")
