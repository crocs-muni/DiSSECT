from sage.all import ZZ
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def i15_curve_function(curve: CustomCurve):
    try:
        return {"a": ZZ(curve.a()), "b": ZZ(curve.b())}
    except (TypeError, ValueError):
        return {"a":None, "b":None}

def compute_i15_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "i15", i15_curve_function, desc=desc, verbose=verbose)
