from sage.all import PolynomialRing, GF

from dissect.traits.a05.a05 import ext_card, is_torsion_cyclic
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def eigenvalues(curve: CustomCurve, l, s=1):
    """Computes the eigenvalues of Frobenius endomorphism in F_l, or in F_l if s=2"""
    x = PolynomialRing(GF(l ** s), 'x').gen()
    q = curve.q
    t = curve.trace
    f = x ** 2 - t * x + q
    return f.roots()


def i_finder(curve: CustomCurve, l):
    """
    Finds the minimal degrees i_2,i_1 of extension of curve E/F_q where
    E/F_q**(i_2) - all l+1 isogenies are rational, E/F_q**(i_1) - at least 1 isogeny is rational
    Returns i2, i1
    """
    eig = eigenvalues(curve, l)
    # Case with no eigenvalues
    if not eig:
        eig = eigenvalues(curve, l, s=2)
        a, b = eig[0][0], eig[1][0]
        i2 = (a * b ** (-1)).multiplicative_order()
        i1 = i2
        return i2, i1

    a = eig[0][0]
    # Case with 2 eigenvalues
    if len(eig) == 2:
        b = eig[1][0]
        i1 = 1
        i2 = (a * b ** (-1)).multiplicative_order()
        return i2, i1
    # Case with 1 eigenvalue
    i1 = 1
    i2 = 1
    deg = a.multiplicative_order()
    card = ext_card(curve, deg)
    if card % l ** 2 != 0 or is_torsion_cyclic(curve, l, deg):
        i2 *= l
    return i2, i1


def a24_curve_function(curve, l):
    """
    Computes i2,i1 (see i_finder) for all primes l<l_max
    Returns a dictionary (keys: 'least' (i1), 'full' (i2), 'relative' (i2/i1))
    """
    curve_results = {}
    try:
        i2, i1 = i_finder(curve, l)
        least, full, relative = i1, i2, i2 // i1
    except (ArithmeticError, TypeError, ValueError) as _:
        least, full, relative = None, None, None

    curve_results['least'] = least
    curve_results['full'] = full
    curve_results['relative'] = relative
    return curve_results


def compute_a24_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a24', a24_curve_function, desc=desc, verbose=verbose)
