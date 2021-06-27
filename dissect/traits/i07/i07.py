from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
from dissect.utils.json_handler import FLOAT_PRECISION

DISTANCE_32 = "distance 32"
DISTANCE_64 = "distance 64"


def i07_curve_function(curve: CustomCurve):
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
        "ratio": round(float(ratio), FLOAT_PRECISION),
        DISTANCE_32: dist32,
        DISTANCE_64: dist64,
    }
    return curve_results


def compute_i07_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "i07", i07_curve_function, desc=desc, verbose=verbose)
