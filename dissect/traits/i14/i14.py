from sage.all import ZZ
from dissect.utils.custom_curve import CustomCurve


def i14_curve_function(curve: CustomCurve):
    """
    Computation of brainpool overlap
    """

    cut = curve.field_bits() - 160 - 1
    if cut <= 0:
        return None
    try:
        acut = ZZ(curve.a()) & ((1 << cut) - 1)
        bcut = ZZ(curve.b()) >> (curve.field_bits() - cut - 1)
    except (ValueError, TypeError):
        return None
    return {"o": ZZ(acut) - ZZ(bcut)}
