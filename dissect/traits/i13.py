from sage.all import ZZ
from dissect.utils.custom_curve import CustomCurve
from dissect.traits import Trait

class I13(Trait):
    NAME = "i13"
    DESCRIPTION = "Computation of $a^3/b^2$."
    INPUT = {}
    OUTPUT = {
        "r": (int, "Integer r")
    }
    DEFAULT_PARAMS = {}

    def compute(curve: CustomCurve, params):
        """
        Computation of r=a^3/b^2 which is used during the generation in x962, secg, fips and others
        """
        a, b = curve.a(), curve.b()
        return {"r": ZZ(curve.field()((a ** 3) / (b ** 2)))}
