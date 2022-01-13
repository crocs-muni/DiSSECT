from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve



def a01_curve_function(curve: CustomCurve):
    """Returns the order of the prime order subgroup and its cofactor"""
    return {"order":curve.order(), "cofactor":curve.cofactor()}


def compute_a01_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "a01", a01_curve_function, desc=desc, verbose=verbose)
