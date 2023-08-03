from dissect.traits import Trait


class X962InvariantTrait(Trait):
    NAME = "x962_invariant"
    DESCRIPTION = "Computation of $a^3/b^2$."
    INPUT = {}
    OUTPUT = {"r": (int, "Integer r")}
    DEFAULT_PARAMS = {}

    def compute(self, curve, params):
        """
        Computation of r=a^3/b^2 which is used during the generation in x962, secg, fips and others
        """
        from sage.all import ZZ

        a, b = curve.a(), curve.b()
        return {"r": ZZ(curve.field()((a**3) / (b**2)))}


def test_x962_invariant():
    assert True
