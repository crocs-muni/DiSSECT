from sage.all import ceil, log, sqrt, pi, floor, ln, gcd

from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve



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
    cm_disc = curve.cm_discriminant()
    frob_disc_factor = curve.frobenius_disc_factorization()
    if frob_disc_factor.timeout():
        return {"upper": frob_disc_factor, "lower": frob_disc_factor}
    fact_d = [f for f, e in frob_disc_factor.factorization(unpack=False) if e % 2 == 1]
    if cm_disc % 4 == 0:
        fact_d.append(2)

    w = {4: 4, 3: 6}.get(-cm_disc, 2)
    upper_bound = ceil(log(-cm_disc) * sqrt(-cm_disc) * w / (2 * pi))

    fact_d = sorted(fact_d)[:-1]
    lower_bound = 1
    for f in fact_d:
        lower_bound *= (1 - floor(2 * sqrt(f)) / (f + 1)) * ln(-cm_disc)
    if gcd(cm_disc, 5077) == 1:
        lower_bound *= (1 / 55)
    else:
        lower_bound *= (1 / 7000)
    lower_bound = floor(lower_bound)
    curve_results = {"upper": upper_bound, "lower": lower_bound}
    return curve_results


def compute_a08_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "a08", a08_curve_function, desc=desc, verbose=verbose)
