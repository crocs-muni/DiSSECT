from dissect.utils.utils import Factorization
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve

TRAIT_TIMEOUT = 20


def a25_curve_function(curve: CustomCurve, deg):
    """Computation of the trace in an extension together with its factorization"""
    trace = curve.extended_trace(deg)
    f = Factorization(trace, timeout_duration=TRAIT_TIMEOUT)
    num_of_factors = f.timeout_message() if f.timeout() else len(list(set(f.factorization())))
    curve_results = {
        "trace": curve.trace(),
        "trace_factorization": f.factorization(),
        "number_of_factors": num_of_factors,
    }
    return curve_results


def compute_a25_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "a25", a25_curve_function, desc=desc, verbose=verbose)
