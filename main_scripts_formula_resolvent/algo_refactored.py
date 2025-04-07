#!/usr/bin/env python
# coding: utf-8

###############################################################################
# Function: mycollect
###############################################################################
def mycollect(e1, e2):
    """
    Collects e2 coefficients in e1, even when e2 is not a factor of
    some of the terms of e1.
    Assumes a Sage/Maxima environment where maxima_calculus.gensym()._sage_()
    is available.
    """
    g = maxima_calculus.gensym()._sage_()
    while g in e1.variables():
        g = maxima_calculus.gensym()._sage_()
    return sum([v[0]*g^v[1] for v in e1.subs(e2 == g).coefficients(g)]).subs(g == e2)


###############################################################################
# Main script logic
###############################################################################
# Example initial discriminant list (uncomment or modify as needed):
# disc_list = [1, 1, a_1^2 - 4*a_0]

# Degree
deg = 4

# Generate variable names "a_0", "a_1", ...
var_list = ["a_" + str(i) for i in range(deg)]
var(var_list + ["alpha"])  # Sage-specific function to declare symbolic vars

# Example disc_list; make sure it has enough entries if you're indexing disc_list[deg-1]
disc_list = [1, 1, a_1^2 - 4*a_0]  # For deg = 4, disc_list[3] is needed below.

# d_coef: [ (1*2)/2, (2*3)/2, (3*4)/2, ... ] up to deg-1
d_coef = [i*(i+1)/2 for i in range(1, deg)]

# d_sym: last (deg-2) of a_i plus [1]
d_sym = [eval("a_" + str(i)) for i in range(deg)]
d_sym = d_sym[-(deg-2):] + [1]

# d_alpha: [1, alpha, alpha^2, ... ] up to alpha^(deg-2)
d_alpha = [eval("alpha**" + str(i)) for i in range(deg - 1)]

# d_exp = sum of i*j*k for i in d_coef, j in d_sym, k in d_alpha
d_exp = sum([i*j*k for i, j, k in zip(d_coef, d_sym, d_alpha)])

# n_coef initialization
n_coef = [2, 2]
for j in range(deg - 3):
    n_coef.append(0)
    add = list(range(1, j + 4))
    n_coef = [x + y for x, y in zip(n_coef, add)]

# eqb_sym: last (deg-1) of a_i
eqb_sym = [eval("a_" + str(i)) for i in range(deg)]
eqb_sym = eqb_sym[-(deg - 1):]
eqb_exp = sum([i*j*k for i, j, k in zip(n_coef, d_alpha, eqb_sym)])

# eqc_sym uses reversed(d_coef) and first (deg-1) of a_i
d_coef_rev = list(reversed(d_coef))
eqc_sym = [eval("a_" + str(i)) for i in range(deg)]
eqc_sym = eqc_sym[: (deg - 1)]
eqc_exp = sum([i*j*k for i, j, k in zip(d_coef_rev, d_alpha, eqc_sym)])

# Compute ratio, eqb, eqc
ratio = -1/2 * (eqb_exp / d_exp)
eqb = eqb_exp / d_exp
eqc = eqc_exp / d_exp

# formula
formula = ((ratio^2 + eqb*ratio + eqc) * (d_exp^2)).full_simplify().factor()

# Build a "full" expression
coeffs = [eval("a_" + str(i)) for i in range(deg)] + [1]
alphas = [eval("alpha**" + str(i)) for i in range(deg + 1)]
full = sum([x*y for x, y in zip(coeffs, alphas)])

# Collect terms of formula
_ = mycollect(formula, alpha)
tmp = formula

for i in range(deg - 3):
    tmp = mycollect(tmp, alpha)
    leading = tmp.operands()[0].subs({alpha: 1})
    tmp = (tmp - leading * alpha**((deg - 3) - i - 1) * full).full_simplify()

simfo = mycollect(tmp, alpha)
simfo_terms = simfo.operands()

lonely_terms = [term for term in simfo_terms if not(term.has(alpha))]
fixed = [term for term in simfo_terms if term not in lonely_terms] + [sum(lonely_terms)]
fixed_only = [term.subs({alpha: 1}) for term in fixed]
fixed_only_2 = [val / fixed_only[0] for val in fixed_only]

cal_list = list(reversed(fixed_only_2[1:]))
co_list = [eval("a_" + str(i)) for i in range(deg)][:deg - 1]
subi = dict(zip(co_list, cal_list))

# Final discriminant computation and appending to disc_list
disc = (disc_list[deg - 1].subs(subi) * (1/4096) * (fixed_only[0]**6)).full_simplify().factor()
disc_list.append(disc)

print("Final disc_list:", disc_list)
