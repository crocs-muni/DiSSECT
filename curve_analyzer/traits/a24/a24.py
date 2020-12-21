from sage.all import PolynomialRing, GF

from curve_analyzer.traits.a05.a05 import ext_card, is_torsion_cyclic
from curve_analyzer.traits.trait_interface import pretty_print_results, compute_results


def eigenvalues(curve, l, s=1):
    '''Computes the eigenvalues of Frobenius endomorphism in F_l, or in F_l if s=2'''
    x = PolynomialRing(GF(l ** s), 'x').gen()
    q = curve.q
    t = curve.trace
    f = x ** 2 - t * x + q
    return f.roots()


def i_finder(curve, l):
    '''
    Finds the minimal degrees i_2,i_1 of extension of curve E/F_q where
    E/F_q**(i_2) - all l+1 isogenies are rational, E/F_q**(i_1) - at least 1 isogeny is rational
    Returns i2, i1
    '''
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
    E = curve.EC
    q = curve.q
    card = ext_card(q, curve.order * curve.cofactor, deg)
    if card % l ** 2 != 0 or is_torsion_cyclic(E, curve.q, curve.order * curve.cofactor, l, deg, curve.field):
        i2 *= l
    return i2, i1


def a24_curve_function(curve, l):
    '''
    Computes i2,i1 (see i_finder) for all primes l<l_max
    Returns a dictionary (keys: 'least' (i1), 'full' (i2), 'relative' (i2/i1))
    '''
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


def get_a24_captions(results):
    captions = ['least', 'full', 'relative']
    return captions


def select_a24_results(curve_results):
    keys = ['least', 'full', 'relative']
    selected_results = []
    for key in keys:
        selected_key = []
        for x in curve_results:
            selected_key.append(x[key])
        selected_results.append(selected_key)
    return selected_results


def pretty_print_a24_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a24', get_a24_captions, select_a24_results, save_to_txt=save_to_txt)
