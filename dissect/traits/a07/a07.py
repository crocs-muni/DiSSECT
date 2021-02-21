from sage.all import Integers, euler_phi, ZZ

from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def a07_curve_function(curve: CustomCurve):
    """Computes the embedding degree (with respect to the generator order) and its complement"""
    q = curve.q
    l = curve.order
    embedding_degree = (Integers(l)(q)).multiplicative_order()
    embedding_degree_complement = ZZ(euler_phi(l) / embedding_degree)
    complement_bit_length = embedding_degree_complement.nbits()
    curve_results = {"embedding_degree_complement": embedding_degree_complement,
                     "complement_bit_length": complement_bit_length}
    return curve_results


def compute_a07_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a07', a07_curve_function, desc=desc, verbose=verbose)
