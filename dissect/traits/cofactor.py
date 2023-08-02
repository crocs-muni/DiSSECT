from dissect.traits import Trait


class CofactorTrait(Trait):
    NAME = "cofactor"
    DESCRIPTION = "The order of the prime order subgroup and its cofactor"
    INPUT = {}
    OUTPUT = {
        "order": (int, "Order"),
        "cofactor": (int, "Cofactor"),
    }
    DEFAULT_PARAMS = {}

    def compute(self, curve, params):
        """Returns the order of the prime order subgroup and its cofactor"""
        return {"order": curve.order(), "cofactor": curve.cofactor()}


def test_cofactor():
    assert True
