from sage.all import ZZ
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def i14_curve_function(curve: CustomCurve):
    """
    Computation of brainpool overlap
    """

    cut = curve.field_bits() - 160 - 1
    if cut<=0:
        return None
    acut = curve.a() & ((1 << cut) - 1)
    bcut = curve.b() >> (curve.field_bits() - cut - 1)
    return {"o": ZZ(acut)-ZZ(bcut)}


def compute_i14_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "i14", i14_curve_function, desc=desc, verbose=verbose)
