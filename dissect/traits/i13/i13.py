from sage.all import ZZ
from dissect.utils.custom_curve import CustomCurve


def i13_curve_function(curve: CustomCurve):
    """
    Computation of r=a^3/b^2 which is used during the generation in x962, secg, fips and others
    """
    a, b = curve.a(), curve.b()
    return {"r": ZZ(curve.field()((a ** 3) / (b ** 2)))}
