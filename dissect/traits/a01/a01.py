from sage.all import gcd, lcm

from dissect.traits.trait_interface import compute_results, timeout
from dissect.utils.custom_curve import CustomCurve

# global time for one group computation

TIME = 150


def smith_normal_form(ext_ec):
    """compute the smith normal form, (n1,n2) where n1 divides n2"""
    gens = ext_ec.abelian_group().gens()
    if len(gens) == 1:
        return 1, gens[0].order()
    ord1, ord2 = gens[0].order(), gens[1].order()
    return gcd(ord1, ord2), lcm(ord1, ord2)


def a01_curve_function(curve: CustomCurve, deg):
    """returns the orders of the two generators of the curve over the deg-th relative extension"""
    curve_results = {}
    ext_ec = curve.extended_ec(deg)
    result = timeout(smith_normal_form, [ext_ec], timeout_duration=TIME)
    if isinstance(result, str):
        result = result, result
    curve_results["ord1"], curve_results["ord2"] = result
    return curve_results


def compute_a01_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "a01", a01_curve_function, desc=desc, verbose=verbose)
