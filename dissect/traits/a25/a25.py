import dissect.traits.trait_utils as tu
from dissect.traits.trait_interface import compute_results
from dissect.traits.trait_utils import ext_trace
from dissect.utils.custom_curve import CustomCurve

TRAIT_TIMEOUT = 20


def a25_curve_function(curve: CustomCurve, deg):
    """Computation of the trace in an extension together with its factorization"""
    trace = ext_trace(curve, deg)
    f = tu.factorization(trace, timeout_duration=TRAIT_TIMEOUT)
    curve_results = {'trace': curve.trace, 'trace_factorization': f, 'number_of_factors': len(list(set(f)))}
    return curve_results


def compute_a25_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a25', a25_curve_function, desc=desc, verbose=verbose)
