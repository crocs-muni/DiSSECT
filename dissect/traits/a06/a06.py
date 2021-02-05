from sage.all import kronecker

from dissect.traits.a05.a05 import ext_card
from dissect.traits.trait_interface import compute_results


def ext_cm_disc(q, card_low, deg):
    """returns the CM discriminant (up to a square) over deg-th relative extension"""
    card_high = ext_card(q, card_low, deg)
    ext_tr = q ** deg + 1 - card_high
    return ext_tr ** 2 - 4 * q ** deg


def a06_curve_function(curve, l, deg):
    """returns the Kronecker symbol of the CM discriminant over the deg-th relative extension with respect to l"""
    q = curve.q
    curve_results = {}
    order = curve.order * curve.cofactor
    cm_disc = ext_cm_disc(q, order, deg)
    while cm_disc % l ** 2 == 0:
        cm_disc = cm_disc / l ** 2

    if l == 2 and cm_disc % 4 != 1:
        curve_results["kronecker"] = 0
    else:
        curve_results["kronecker"] = kronecker(cm_disc, l)
    return curve_results


def compute_a06_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a06', a06_curve_function, desc=desc, verbose=verbose)
