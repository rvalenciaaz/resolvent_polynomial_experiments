from sage.all import *

# Declare variables for x's and e's.
var_list = ["x" + str(i) for i in range(100)] + ["e" + str(i) for i in range(100)]
var(var_list + ["n","x"])

# Declare symbolic coefficients for the original polynomial.
# Note: we rename the coefficient 'e' to 'e_coef' to avoid conflict with the elementary symmetric variables.
var('a b c d e_coef f g h')

# Define the symmetric functions object (renamed to avoid clashing with the symbolic e's).
e = SymmetricFunctions(QQ).e()  # Not used in our final substitutions.

def ele_dict(deg):
    es = [e[i].expand(deg) for i in range(deg + 1)]
    coe = [eval("e" + str(i)) for i in range(deg + 1)]
    return dict(zip(coe, es))
def root_unity(deg):
    """
    Return a dict with variables as keys and the n-th roots of unity as values.

    INPUT:
    - n: a positive integer

    OUTPUT:
    - A dictionary {x_k: zeta^k} where zeta = e^(2*pi*I / n).
    """
    # Create a primitive n-th root of unity
    zeta = exp(2*pi*I / deg)
    
    # Prepare the dictionary
    roots_dict = {}
    kx= [eval("x" + str(i)) for i in range(deg)]
    # Fill the dictionary with x_k -> zeta^k
    for expo, k in enumerate(kx):
            roots_dict[k] = zeta**expo
    
    return roots_dict

def polexp(n):
    return sum([((-1)**i)*eval("e"+str(i))*(eval("x0")**(n-i)) for i in range(0,n+1)])

def vietas_dict(deg):
    """
    Returns a dictionary mapping the symbolic variables e0, e1, ..., e_deg
    to their values via Vieta's formulas for a monic polynomial.
    
    For example, for a monic polynomial:
      e0 = 1,
      e1 = -a,
      e2 = b,
      e3 = -c,
      e4 = d,
      e5 = -e_coef,
      e6 = f,
      e7 = -g,
      e8 = h,
      ...
    
    Coefficients are taken in order from the list: [a, b, c, d, e_coef, f, g, h].
    """
    coeff_symbols = [a, b, c, d, e_coef, f, g, h, i]  # Coefficients in order.
    subs_dict = {}
    for k in range(deg+1):
        # Retrieve the symbolic variable e0, e1, ... from the global namespace.
        ek = globals()["e"+str(k)]
        #if k == 0:
        #    subs_dict[ek] = 1
        #else:
        subs_dict[ek] = (-1)**k * coeff_symbols[k]
    return subs_dict

def asum(n):
    return sum(
        (-1)**k * ((n - k - 1) * (n - k)) * x0**(n - k - 2) * globals()["e"+str(k)]
        for k in range(0, n-1)
    )

def bsum(n):
    return sum(
        (-1)**k * k * (n - k) * x0**(n - k - 1) * globals()["e"+str(k)]
        for k in range(1, n)
    )

def csum(n):
    return sum(
        (-1)**k * (k * (k - 1)) * x0**(n - k) * globals()["e"+str(k)]
        for k in range(2, n+1)
    )

#print(vietas_dict(4))
#print(root_unity(4))	
for j in range(3, 9):

    polyno=polexp(j).subs({e0:1})    

    formula = (bsum(j)**2 - asum(j) * csum(j))/(j-1)**2
    
    # Group the expression by powers of x0.
    grouped_formula = formula.collect(x0).subs({e0:1})
    
    # Generate LaTeX code for the grouped formula.
    latex_grouped_formula = latex(grouped_formula)
    
    # Substitute the elementary symmetric variables with Vieta's formulas.
    substituted = formula.subs(vietas_dict(j)).full_simplify().factor()
    
    grouped_subs= substituted.collect(x0).subs({a:1})
    
    subs_ele = formula.subs(ele_dict(j)).full_simplify().factor()
    
    new1=grouped_formula.operands()

    lonely_terms = [term for term in new1 if not(term.has(x0))]

    fixed = [term for term in new1 if term not in lonely_terms] + [sum(lonely_terms)]
    
    leading = fixed[0].subs({x0:1})
    
    if j>=4:
        diff=grouped_formula
        for cou in range(0,j-3):
            #print("\ntmp\n")
            #print(leading)
            subi=(leading*(polyno*x0**(j-4-cou)).collect(x0).simplify())  
            #print(subi)
            #print("\n")
            diff=(diff-subi).collect(x0).simplify()
            #print(diff)
            new1=diff.operands()

            lonely_terms = [term for term in new1 if not(term.has(x0))]

            fixed = [term for term in new1 if term not in lonely_terms] + [sum(lonely_terms)]

            leading = fixed[0].subs({x0:1})
            new1=diff.operands()
    else:
        new2=new1
        new1=new2
    
    lonely_terms = [term for term in new1 if not(term.has(x0))]
    
    fixed = [term for term in new1 if term not in lonely_terms] + [sum(lonely_terms)]
    
    leading = fixed[0].subs({x0:1})
    div_leading = [val / fixed[0].subs({x0:1}) for val in fixed]
    print("Degree j =", j)
    print("\nPolynomial")
    print(polyno)
    print("\nGrouped formula (by powers of x₀):")
    print(grouped_formula)
    print("\nLaTeX code for grouped formula:")
    print(latex_grouped_formula)
    print("\nAfter substitution using Vieta's formulas:")
    print(grouped_subs)
    print("\nLaTeX code for grouped vieta:")
    print(latex(grouped_subs))
    print("\n Results after substitution for roots variables")
    print(subs_ele)
    print("\n Substracting the original polynomial\n")
    print(fixed)
    print("\n")
    print(sum(fixed).subs(vietas_dict(j)).collect(x0))
    print("\n")
    print(sum(div_leading).subs(vietas_dict(j)).collect(x0).subs({x0:x}))
    print("\n")
    print(sum(div_leading).collect(x0).subs({x0:x}))
    print("\n Leading term \n")
    print(leading)
    print("\n")
    lea_roots=leading.subs(ele_dict(j)).simplify().factor()
    print(lea_roots)
    print("\n")
    lea_uni=lea_roots.subs(root_unity(j)).simplify().factor()
    print(N(lea_uni))
    print("\n")
    print("\n" + "="*50 + "\n")
