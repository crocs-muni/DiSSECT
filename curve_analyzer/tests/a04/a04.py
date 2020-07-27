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
    curve_results = {'plus': {}, 'minus': {}}
    curve_results['plus']['factorization'] = near_order_factorizations(curve.order, '+', k, t)
    curve_results['plus']['largest_factor_bitlen'] = largest_factor_bitlen(curve_results['plus']['factorization'])
    curve_results['minus']['factorization'] = near_order_factorizations(curve.order, '-', k, t)
    curve_results['minus']['largest_factor_bitlen'] = largest_factor_bitlen(curve_results['minus']['factorization'])
    return curve_results


def compute_a04_results(curve_list, k_max=10, order_bound=256, overwrite=False, desc=''):
    global_params = {"k_max": range(1, k_max + 1)}
    params_local_names = ["k"]
    compute_results(curve_list, 'a04', a04_curve_function, global_params, params_local_names, order_bound, overwrite,
                    desc=desc)


def get_a04_captions(results):
    captions = [['plus', 'largest_factor_bitlen'], ['minus', 'largest_factor_bitlen']], ['largest_factor_bitlen (+)',
                                                                                         'largest_factor_bitlen (-)']
    return captions


def select_a04_results(curve_results):
    selected_results = []
    for key in curve_results.keys():
        selected_results.append(curve_results[key])
    return selected_results


def pretty_print_a04_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a04', get_a04_captions, select_a04_results, save_to_txt=save_to_txt)
