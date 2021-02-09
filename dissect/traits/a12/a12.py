from sage.all import Integers, ZZ, euler_phi

from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def a12_curve_function(curve: CustomCurve, l):
    """
    Computes the order of l (small prime) modulo curve order and bit length of the index of <l>
    Returns a dictionary
    """
    card = curve.cardinality
    try:
        mul_ord = (Integers(card)(l)).multiplicative_order()
        complement_bit_length = ZZ(euler_phi(card) / mul_ord).nbits()
    except ArithmeticError:
        mul_ord = None
        complement_bit_length = None
    curve_results = {'order': mul_ord, 'complement_bit_length': complement_bit_length}
    return curve_results


def compute_a12_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a12', a12_curve_function, desc=desc, verbose=verbose)
