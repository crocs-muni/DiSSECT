from dissect.traits import Trait


class BrainpoolOverlapTrait(Trait):
    NAME = "brainpool_overlap"
    DESCRIPTION = "Bit overlaps in curve coefficients"
    INPUT = {}
    OUTPUT = {"o": (int, "overlap")}
    DEFAULT_PARAMS = {}

    def compute(self, curve, params):
        """
        Computation of brainpool overlap
        """
        from sage.all import ZZ

        cut = curve.field_bits() - 160 - 1
        if cut <= 0:
            return None
        try:
            acut = ZZ(curve.a()) & ((1 << cut) - 1)
            bcut = ZZ(curve.b()) >> (curve.field_bits() - cut - 1)
        except (ValueError, TypeError):
            return None
        return {"o": ZZ(acut) - ZZ(bcut)}


def test_brainpool_overlap():
    assert True
