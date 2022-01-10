from sage.all import ZZ
from dissect.utils.custom_curve import CustomCurve


def i15_curve_function(curve: CustomCurve):
    try:
        return {"a": ZZ(curve.a()), "b": ZZ(curve.b())}
    except (TypeError, ValueError):
        return {"a":None, "b":None}
