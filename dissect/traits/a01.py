from dissect.traits import Trait


class A01(Trait):
    NAME = "a01"
    DESCRIPTION = "The order of the prime order subgroup and its cofactor",
    INPUT = {}
    OUTPUT = {
        "order": (int, "Order"),
        "cofactor": (int, "Cofactor"),
    }
    DEFAULT_PARAMS = {}

    def compute(self, curve, params):
        """Returns the order of the prime order subgroup and its cofactor"""
        return { "order": curve.order(), "cofactor": curve.cofactor() }


def test_a01():
    assert True
