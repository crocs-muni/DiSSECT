from sage.all import factor

from curve_analyzer.traits.a02.a02 import ext_trace
from curve_analyzer.traits.trait_interface import compute_results


def a25_curve_function(curve, deg):
    '''Computation of the trace in an extension together with its factorization'''
    trace = ext_trace(curve.q, curve.trace, deg)
    f = list(factor(trace))
    f = [list(i) for i in f]
    curve_results = {'trace': curve.trace, 'trace_factorization': f, 'number_of_factors': len(f)}
    return curve_results


def compute_a25_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a25', a25_curve_function, desc=desc, verbose=verbose)
