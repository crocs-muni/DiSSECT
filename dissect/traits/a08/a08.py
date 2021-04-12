from sage.all import ceil, log, sqrt, pi, floor, ln, gcd

from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
from dissect.traits.trait_utils import squarefree_and_factorization


def a08_curve_function(curve: CustomCurve):
    """
    Computes the lower and upper bound of class number of the maximal order of the endomorphism algebra

    Upper bound:
    Inequality class number<= sqrt(d)*log(d)*constant (see below)
    #https://en.wikipedia.org/wiki/Class_number_formula#Dirichlet_class_number_formula
    #https://math.stackexchange.com/questions/1887252/class-number-upper-bound-for-imaginary-quadratic-fields

    Lower bound:
    https://mathworld.wolfram.com/ClassNumber.html

    """
    q = curve.q
    trace = curve.trace
    D = trace ** 2 - 4 * q
    d, fact = squarefree_and_factorization(D)
    fact_d = [f for f in set(fact) if fact.count(f) % 2 == 1]
    if d % 4 != 1:
        d *= 4
        fact_d.append(2)

    w = {4: 4, 3: 6}.get(-d, 2)
    upper_bound = ceil(log(-d) * sqrt(-d) * w / (2 * pi))

    fact_d = sorted(fact_d)[:-1]
    lower_bound = 1
    for f in fact_d:
        lower_bound *= (1 - floor(2 * sqrt(f)) / (f + 1)) * ln(-d)
    if gcd(d, 5077) == 1:
        lower_bound *= (1 / 55)
    else:
        lower_bound *= (1 / 7000)
    lower_bound = floor(lower_bound)
    curve_results = {"upper": upper_bound, "lower": lower_bound}
    return curve_results


def compute_a08_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "a08", a08_curve_function, desc=desc, verbose=verbose)
