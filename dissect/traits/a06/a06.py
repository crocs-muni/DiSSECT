from sage.all import ZZ, sqrt

from dissect.traits.trait_interface import compute_results
from dissect.traits.trait_utils import ext_cm_disc
import dissect.traits.trait_utils as tu
from dissect.utils.custom_curve import CustomCurve

TIME=30

def a06_curve_function(curve: CustomCurve, deg):
    """returns the factorization of the D_deg/D_1, where D_deg is the CM discriminant over the deg-th relative
    extension with respect to l """
    curve_results = {}
    cm_disc_base = ext_cm_disc(curve, deg=1)
    cm_disc_ext = ext_cm_disc(curve, deg=deg)
    ratio_sqrt = ZZ(sqrt(cm_disc_ext / cm_disc_base))
    curve_results["ratio_sqrt"] = ratio_sqrt
    curve_results["factorization"] = tu.factorization(ratio_sqrt, timeout_duration=TIME)
    return curve_results


def compute_a06_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a06', a06_curve_function, desc=desc, verbose=verbose)
