from sage.all import prime_range, Integers, ZZ
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


def a12_curve_function(curve, l):
    mul_ord = (Integers(curve.order)(l)).multiplicative_order()
    curve_results = {'order': mul_ord}
    tmp = (curve.order - 1) / curve_results['order']
    curve_results['complement_bit_length'] = ZZ(tmp).nbits()
    return curve_results


def compute_a12_results(curve_list, l_max=100, order_bound=256, overwrite=False, desc=''):
    global_params = {'l_max': prime_range(l_max)}
    params_local_names = ['l']
    compute_results(curve_list, 'a12', a12_curve_function, global_params, params_local_names, order_bound, overwrite,
                    desc=desc)


def get_a12_captions(results):
    captions = ['order', 'complement_bit_length']
    return captions


def select_a12_results(curve_results):
    selected_results = []
    for key in curve_results.keys():
        selected_results.append(curve_results[key])
    return selected_results


def pretty_print_a12_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a12', get_a12_captions, select_a12_results, save_to_txt=save_to_txt)
