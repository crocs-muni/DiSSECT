from sage.all import ZZ, GF

from dissect.utils.custom_curve import CustomCurve
from dissect.utils.json_handler import FLOAT_PRECISION
from dissect.traits import Trait


class I08(Trait):
    NAME = "i08"
    DESCRIPTION = "Bitlength of the $x$-coordinate of small inverted generator scalar multiples, i.e. $x$-coordinate of $P$ where $kP=G$. The difference and ratio to the bitlength of the whole group is also considered."
    INPUT = {
        "k": (int, "Integer")
    }
    OUTPUT = {
        "Hx": (int, "x-coordinate"),
        "bits": (int, "Bitlength of x"),
        "difference": (int, "Difference"),
        "ratio": (float, "Ratio")
    }
    DEFAULT_PARAMS = {
        "k": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }


    def compute(curve: CustomCurve, params):
        """Computes the bit length of the x-coordinate of the generator multiplied by 1/k"""
        G = curve.generator()
        if G is None:
            return {"Hx": None, "bits": None, "difference": None, "ratio": None}
        F = GF(curve.order())
        multiple = F(1) / params["k"]
        H = ZZ(multiple) * G
        try:
            Hx = ZZ(H[0])
        except TypeError:
            return {"Hx": None, "bits": None, "difference": None, "ratio": None}
        bits = Hx.nbits()
        difference = ZZ(curve.cardinality()).nbits() - bits
        ratio = bits / curve.nbits()
        curve_results = {
            "Hx": Hx,
            "bits": bits,
            "difference": difference,
            "ratio": round(ratio, FLOAT_PRECISION),
        }
        return curve_results
