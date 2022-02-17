from sage.all import ZZ
from dissect.utils.custom_curve import CustomCurve
from dissect.traits import Trait

class I15(Trait):
    NAME = "i15"
    DESCRIPTION = "Coefficients of the curve in Weierstrass form"
    INPUT = {}
    OUTPUT = {
        "a": (int, "a"),
        "b": (int, "b")
    }
    DEFAULT_PARAMS = {}

    def compute(curve: CustomCurve, params):
        try:
            return {"a": ZZ(curve.a()), "b": ZZ(curve.b())}
        except (TypeError, ValueError):
            return {"a":None, "b":None}
