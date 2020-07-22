from sage.all_cmdline import *   # import sage library
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


def mult_ord_gen(order, l_max):
    for l in prime_range(l_max):
        try:
            yield Mod(l, order).multiplicative_order()
        except TypeError as e:
            yield None

def a12_curve_function(curve, l_max):
    curve_results = {}
    curve_results['orders'] = [mult_ord for mult_ord in mult_ord_gen(curve.order, l_max)]
    curve_results['complement_bit_lengths'] = [ZZ((curve.order-1 )/x).nbits() for x in curve_results['orders']]
    return curve_results

def compute_a12_results(curve_list, l_max = 100 , order_bound = 256 , overwrite = False):
    parameters = {'l_max': l_max}
    compute_results('a12', a12_curve_function, parameters, order_bound, overwrite, curve_list = curve_list)

def pretty_print_a12_results(curve_list, save_to_txt = True):
    pretty_print_results('a12', [['complement_bit_lengths']], ['complement bitlens'], save_to_txt = save_to_txt, curve_list = curve_list)

