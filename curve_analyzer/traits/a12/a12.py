from sage.all import Integers, ZZ, euler_phi

from curve_analyzer.traits.trait_interface import pretty_print_results, compute_results


def a12_curve_function(curve, l):
    '''
    Computes the order of l (small prime) modulo curve order and bit length of the index of <l>
    Returns a dictionary
    '''
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


def get_a12_captions(results):
    captions = ['order', 'complement_bit_length']
    return captions


def select_a12_results(curve_results):
    keys = ['order', 'complement_bit_length']
    selected_results = []
    for key in keys:
        selected_key = []
        for x in curve_results:
            selected_key.append(x[key])
        selected_results.append(selected_key)
    return selected_results


def pretty_print_a12_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a12', get_a12_captions, select_a12_results, save_to_txt=save_to_txt)
