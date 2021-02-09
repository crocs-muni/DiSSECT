from sage.all import sqrt

import dissect.traits.trait_utils as tu
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve

TRAIT_TIMEOUT = 30


def i06_curve_function(curve: CustomCurve):
    """"Computes the square part of 4*p-1. 4*order-1 (result is square root of the square part)"""
    order = curve.order  # * curve.cofactor
    q = curve.q
    a = 4 * q - 1
    b = 4 * order - 1
    a_squarefree_part = tu.squarefree_part(a, timeout_duration=TRAIT_TIMEOUT, use_ecm=False)
    b_squarefree_part = tu.squarefree_part(b, timeout_duration=TRAIT_TIMEOUT, use_ecm=False)
    if a_squarefree_part == 'NO DATA (timed out)':
        a_square_part = a_squarefree_part
    else:
        a_square_part = sqrt(a // a_squarefree_part)
    if b_squarefree_part == 'NO DATA (timed out)':
        b_square_part = b_squarefree_part
    else:
        b_square_part = sqrt(b // b_squarefree_part)
    curve_results = {"p": a_square_part, "order": b_square_part}
    return curve_results


def compute_i06_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'i06', i06_curve_function, desc=desc, verbose=verbose)
