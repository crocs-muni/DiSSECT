from sage.all import ecm

from curve_analyzer.tests.test_interface import pretty_print_results, compute_results, timeout

# global time for one factorization
TIME = 10


def attempt_factor(n, t):
    '''Factors 'n' in time 't' '''
    try:
        factorization = timeout(ecm.factor, [n], timeout_duration=t)
    except:
        factorization = None
    return factorization


def near_order_factorizations(n, sign='+', k=10, t=10):
    '''Computer factorization of k*n+1 (k*n-1) if 'sign' is "+" ("-") in time 't' '''
    assert sign in ['+', '-']

    if sign == '+':
        m = k * n + 1
    else:
        m = k * n - 1
    try:
        return attempt_factor(m, t)
    except:
        return None


def largest_factor_bitlen(factorization):
    '''Computes bit length of largest factor(last item of list) of 'factorization' '''
    try:
        bitlen = factorization[-1].nbits()
    except:
        bitlen = factorization
    return bitlen


def a04_curve_function(curve, k):
    '''
    Computes factorization of ord*k+1 and ord*k-1 and bit lengths of their largest factors
    Returns a dictionary
    noinspection PyDictCreation
    '''
    card = curve.cardinality
    t = TIME
    curve_results = {}
    curve_results['(+)factorization'] = near_order_factorizations(card, '+', k, t)
    curve_results['(+)largest_factor_bitlen'] = largest_factor_bitlen(curve_results['(+)factorization'])
    curve_results['(-)factorization'] = near_order_factorizations(card, '-', k, t)
    curve_results['(-)largest_factor_bitlen'] = largest_factor_bitlen(curve_results['(-)factorization'])
    return curve_results


def compute_a04_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a04', a04_curve_function, desc=desc, verbose=verbose)


def get_a04_captions(results):
    captions = ['factorization (+)', 'largest_factor_bitlen (+)', ' factorization (-)', 'largest_factor_bitlen (-)']
    return captions


def select_a04_results(curve_results):
    keys = [('(+)' + 'factorization'), ('(+)' + 'largest_factor_bitlen'), ('(-)' + 'factorization'),
            ('(-)' + 'largest_factor_bitlen')]
    selected_results = []
    for key in keys:
        selected_key = []
        for x in curve_results:
            selected_key.append(x[key])
        selected_results.append(selected_key)
    return selected_results


def pretty_print_a04_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a04', get_a04_captions, select_a04_results, save_to_txt=save_to_txt)
