from sage.all import ZZ
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def i13_curve_function(curve: CustomCurve):
    """
    Computation of r=a^3/b^2 which is used during the generation in x962, secg, fips and others
    """
    a, b = curve.a(), curve.b()
    return {"r": ZZ(curve.field()((a ** 3) / (b ** 2)))}


def compute_i13_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "i13", i13_curve_function, desc=desc, verbose=verbose)
