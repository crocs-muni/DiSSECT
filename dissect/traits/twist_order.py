from typing import List
from dissect.traits import Trait

TRAIT_TIMEOUT = 30


class TwistOrderTrait(Trait):
    NAME = "twist_order"
    DESCRIPTION = "Factorization of the quadratic twist cardinality in an extension, i.e. $\\#E(\\mathbb{F}_{p^d})$."
    INPUT = {
        "deg": (int, "Degree of extension")
    }
    OUTPUT = {
        "twist_cardinality": (int, "Twist cardinality"),
        "factorization": (List[int], "Factorization of the cardinality")
    }
    DEFAULT_PARAMS = {
        "deg": [1, 2]
    }


    def compute(curve, params):
        """Returns the factorization of the cardinality of the quadratic twist of the curve"""
        from dissect.utils.utils import Factorization

        tr = curve.extended_trace(params["deg"])
        card = curve.extended_cardinality(params["deg"])
        twist_card = card + 2 * tr
        f = Factorization(twist_card, timeout_duration=TRAIT_TIMEOUT)

        curve_results = {"twist_cardinality": twist_card, "factorization": f.factorization()}
        return curve_results


def test_twist_order():
    assert True
