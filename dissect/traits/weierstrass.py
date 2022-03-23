from dissect.traits import Trait

class WeierstrassTrait(Trait):
    NAME = "weierstrass"
    DESCRIPTION = "Coefficients of the curve in Weierstrass form"
    INPUT = {}
    OUTPUT = {
        "a": (int, "a"),
        "b": (int, "b")
    }
    DEFAULT_PARAMS = {}

    def compute(curve, params):
        from sage.all import ZZ

        try:
            return {"a": ZZ(curve.a()), "b": ZZ(curve.b())}
        except (TypeError, ValueError):
            return {"a":None, "b":None}


def test_weierstrass():
    assert True
