from sage.all import ecm
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results, remove_values_from_list, timeout, \
    ints_before_strings

TIME = 10


# Factors 'n' in time 't'
def attempt_factor(n, t):
    try:
        factorization = timeout(ecm.factor, [n], timeout_duration=t)
    except:
        factorization = None
    return factorization


# Computer factorization of k*n+1 (k*n-1) if 'sign' is "+" ("-") in time 't'
def near_order_factorizations(n, sign='+', k=10, t=10):
    assert sign in ['+', '-']

    if sign == '+':
        m = k * n + 1
    elif sign == '-':
        m = k * n - 1
    try:
        return attempt_factor(m, t)
    except:
        return None


# Computes bit length of largest factor(last item of list) of 'factorization'
def largest_factor_bitlen(factorization):
    try:
        bitlen = factorization[-1].nbits()
    except:
        bitlen = '-'
    return bitlen


# Computes factorization of ord*k+1 and ord*k-1 and bit lengths of their largest factors
# Returns a dictionary
def a04_curve_function(curve, k):
    t = TIME
    curve_results = {('(+)'+'factorization'): near_order_factorizations(curve.order, '+', k, t)}
    curve_results[('(+)'+'largest_factor_bitlen')] = largest_factor_bitlen(curve_results[('(+)'+'factorization')])
    curve_results[('(-)'+'factorization')] = near_order_factorizations(curve.order, '-', k, t)
    curve_results[('(-)'+'largest_factor_bitlen')] = largest_factor_bitlen(curve_results[('(-)'+'factorization')])
    return curve_results


def compute_a04_results(curve_list, k_max=10, order_bound=256, desc=''):
    global_params = {"k_max": range(1, k_max + 1)}
    params_local_names = ["k"]
    compute_results(curve_list, 'a04', a04_curve_function, global_params, params_local_names, order_bound, desc=desc)


def get_a04_captions(results):
    captions = ['factorization (+)', 'largest_factor_bitlen (+)', ' factorization (-)','largest_factor_bitlen (-)']
    return captions


def select_a04_results(curve_results):
    keys = [('(+)'+'factorization'),('(+)'+'largest_factor_bitlen'),('(-)'+'factorization'),('(-)'+'largest_factor_bitlen')]
    selected_results = []
    for key in keys:
        selected_key = []
        for x in curve_results:
            selected_key.append(x[key])
        selected_results.append(selected_key)
    return selected_results


def pretty_print_a04_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a04', get_a04_captions, select_a04_results, save_to_txt=save_to_txt)
