from typing import List
from dissect.traits import Trait


TRAIT_TIMEOUT = 60

class A06(Trait):
    NAME = "a06"
    DESCRIPTION = "Factorization of ratio of the maximal conductors of CM-field over an extension and over a basefield."
    MOTIVATION = "The prime factors of the ratio determine for which $l$ does the $l$-crater of the curve grows in the given extension."
    INPUT = {
        "deg": (int, "Integer")
    }
    OUTPUT = {
        "factorization": (List[int], "Factorization"),
        "ratio_sqrt": (int, "Ratio sqrt")
    }
    DEFAULT_PARAMS = {
        "deg": [2, 3, 4]
    }

    def compute(curve, params):
        """returns the factorization of the D_deg/D_1, where D_deg is the discriminant over the deg-th relative
        extension"""
        from sage.all import ZZ, sqrt
        from dissect.utils.utils import Factorization

        curve_results = {}
        disc_base = curve.extended_frobenius_disc()
        disc_ext =  curve.extended_frobenius_disc(deg)
        ratio_sqrt = ZZ(sqrt(disc_ext / disc_base))
        curve_results["ratio_sqrt"] = ratio_sqrt
        curve_results["factorization"] = Factorization(ratio_sqrt, timeout_duration=TRAIT_TIMEOUT).factorization()
        return curve_results


def test_a06():
    assert True
