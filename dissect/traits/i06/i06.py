from sage.all import sqrt
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
import dissect.traits.trait_utils as tu


def i06_curve_function(curve: CustomCurve):
    """"Computes the square part of 4*p-1. 4*order-1 (result is square root of the square part)"""
    order = curve.order  # * curve.cofactor
    q = curve.q
    a = 4 * q - 1
    b = 4 * order - 1
    if tu.squarefree_part(a) == 'NO DATA (timed out)':
        a_square_part = 'NO DATA (timed out)'
    else:
        a_square_part = sqrt(a // tu.squarefree_part(a))
    if tu.squarefree_part(b) == 'NO DATA (timed out)':
        b_square_part = 'NO DATA (timed out)'
    else:
        b_square_part = sqrt(b // tu.squarefree_part(b))
    curve_results = {"p": a_square_part, "order": b_square_part}
    return curve_results


def compute_i06_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'i06', i06_curve_function, desc=desc, verbose=verbose)
