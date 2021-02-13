from dissect.traits.a05.a05 import ext_card, is_torsion_cyclic
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
from dissect.traits.trait_utils import eigenvalues


def isogeny_finder(curve: CustomCurve, l):
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
    # deg = k1
    card = ext_card(curve, deg)
    # now check whether k1=k2:
    if card % l ** 2 != 0 or is_torsion_cyclic(curve, l, deg):
        i2 *= l
    return i2, i1


def a24_curve_function(curve, l):
    """
    Computes i2,i1 (see i_finder) for all primes l<l_max
    Returns a dictionary (keys: 'least' (i1), 'full' (i2), 'relative' (i2/i1))
    """
    if curve.q%l==0:
        return {'least': None, 'full': None, 'relative': None} 
    i2, i1 = isogeny_finder(curve, l)
    return {'least': i1, 'full': i2, 'relative': i2 // i1}


def compute_a24_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a24', a24_curve_function, desc=desc, verbose=verbose)
