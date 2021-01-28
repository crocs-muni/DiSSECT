from sage.all import ecm

from curve_analyzer.traits.trait_interface import compute_results, timeout

# global time for one factorization
TIME = 10


def near_order_factorizations(n, sign='+', k=10, t=10):
    """Computer factorization of k*n+1 (k*n-1) if 'sign' is "+" ("-") in time 't' """
    assert sign in ['+', '-']

    if sign == '+':
        m = k * n + 1
    else:
        m = k * n - 1
    return timeout(ecm.factor, [m], timeout_duration=t)


def largest_factor_bitlen(factorization):
    """Computes bit length of largest factor(last item of list) of 'factorization' """
    try:
        bitlen = factorization[-1].nbits()
    except AttributeError:
        bitlen = factorization
    return bitlen


def a04_curve_function(curve, k):
    """
    Computes factorization of ord*k+1 and ord*k-1 and bit lengths of their largest factors
    Returns a dictionary
    """
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
