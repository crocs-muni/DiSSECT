from dissect.traits import Trait

TRAIT_TIMEOUT = 30

class I06(Trait):
    NAME = "i06"
    DESCRIPTION = "Square parts of $4q \\pm 1$ and $4n \\pm 1$."
    INPUT = {}
    OUTPUT = {
        "p": (int, "p"),
        "order": (int, "Order")
    }
    DEFAULT_PARAMS = {}

    def compute(curve, params):
        """"Computes the square root of the square part of 4*p-1 and 4*generator_order-1 """
        from dissect.utils.utils import Factorization

        order = curve.order()
        q = curve.q()
        curve_results = {"p": Factorization(4 * q - 1, use_ecm=False, timeout_duration=TRAIT_TIMEOUT).square_root(),
            "order": Factorization(4 * order - 1, use_ecm=False, timeout_duration=TRAIT_TIMEOUT).square_root()}
        return curve_results


def test_i06():
    assert True
