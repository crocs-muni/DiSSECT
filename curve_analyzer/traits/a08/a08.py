from sage.all import PolynomialRing, NumberField, ZZ

from curve_analyzer.traits.trait_interface import compute_results


def a08_curve_function(curve):
    """
    Computes the class number of the maximal order of the endomorphism algebra
    Time consuming
    """
    q = curve.q
    trace = curve.trace
    Q = PolynomialRing(ZZ, 'x')
    x = Q.gen()
    f = x ** 2 - trace * x + q
    K = NumberField(f, 'c')
    h = K.class_number()
    curve_results = {"class_number": h}
    return curve_results


def compute_a08_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a08', a08_curve_function, desc=desc, verbose=verbose)
