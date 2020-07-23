from sage.all import ecm
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results, remove_values_from_list, timeout, \
    ints_before_strings


def attempt_factor(n, t):
    try:
        factorization = timeout(ecm.factor, [n], timeout_duration=t)
    except:
        factorization = None
    return factorization


# Factorizations (lists of prime factors) of k*n+-1 where k=1,..,k_max
# Returns list of lists
def near_order_factorizations(n, sign='+', k_max=10, t=10):
    factorizations = []
    assert sign in ['+', '-']
    for k in range(1, k_max + 1):
        if sign == '+':
            m = k * n + 1
        elif sign == '-':
            m = k * n - 1
        try:
            factorizations.append(attempt_factor(m, t))
        except:
            continue
    return factorizations


def largest_factor_bitlen(factorization):
    try:
        bitlen = factorization[-1].nbits()
    except:
        bitlen = '-'
    return bitlen


def a4_curve_function(curve, k_max, t):
    curve_results = {'plus': {}, 'minus': {}}
    curve_results['plus']['factorizations'] = near_order_factorizations(curve.order, '+', k_max, t)
    curve_results['plus']['largest_factor_bitlens'] = list(
        map(largest_factor_bitlen, curve_results['plus']['factorizations']))
    curve_results['plus']['min_largest_factor_bitlen'] = min(
        remove_values_from_list(curve_results['plus']['largest_factor_bitlens'], '-'))
    curve_results['minus']['factorizations'] = near_order_factorizations(curve.order, '-', k_max, t)
    curve_results['minus']['largest_factor_bitlens'] = list(
        map(largest_factor_bitlen, curve_results['minus']['factorizations']))
    curve_results['minus']['min_largest_factor_bitlen'] = min(
        remove_values_from_list(curve_results['minus']['largest_factor_bitlens'], '-'))
    return curve_results


def compute_a4_results(curve_list, k_max=10, t=10, order_bound=256, overwrite=False):
    parameters = {'k_max': k_max, 't': t}
    compute_results(curve_list, 'a4', a4_curve_function, parameters, order_bound, overwrite)


def pretty_print_a4_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a4', [['plus', 'largest_factor_bitlens'], ['minus', 'largest_factor_bitlens']],
                         ['largest_factor_bitlens (+)', 'largest_factor_bitlens (-)'], res_sort_key=ints_before_strings,
                         save_to_txt=save_to_txt)
