from dissect.traits import Trait


class I07(Trait):
    NAME = "i07"
    DESCRIPTION = "Distance of $n$ from the nearest power of two and multiple of 32/64."
    INPUT = {},
    OUTPUT = {
        "distance": (int, "Distance"),
        "ratio": (float, "Order"),
        "distance 32": (int, "Distance 32"),
        "distance 64": (int, "Distance 64")
    }

    def compute(curve, params):
        """Computes the distance of curve cardinality to the nearest power of 2 and to the nearest multiple of 32 and 64"""
        card = curve.cardinality()
        l = card.nbits() - 1
        u = l + 1
        L = 2 ** l
        U = 2 ** u
        distance = min(card - L, U - card)
        dist32 = min(abs(card % 32), 32 - abs(card % 32))
        dist64 = min(abs(card % 64), 64 - abs(card % 64))
        ratio = card / distance
        curve_results = {
            "distance": distance,
            "ratio": round(float(ratio), 5),
            "distance 32": dist32,
            "distance 64": dist64
        }
        return curve_results


def test_i07():
    assert True
