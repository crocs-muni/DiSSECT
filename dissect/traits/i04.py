#!/usr/bin/env python3

from sage.all import ZZ, binomial

from dissect.utils.custom_curve import CustomCurve
from dissect.utils.json_handler import FLOAT_PRECISION
from dissect.traits import Trait

def next_hamming(val):
    c = val & -val
    r = val + c
    return ZZ((((r ^ val) >> 2) // c) | r)

class I04(Trait):
    NAME = "i04"
    DESCRIPTION = "Number of points with low Hamming weight of the $x$-coordinate and the expected weight."
    INPUT = {
        "weight": (int, "Integer")
    }
    OUTPUT = {
        "x_coord_count": (int, "X coordinate weight"),
        "expected": (int, "Expected"),
        "ratio": (float, "Ratio")
    }
    DEFAULT_PARAMS = {
        "weight": [1, 2, 3]
    }


    def compute(curve: CustomCurve, params):
        """Computes the number of curve points whose x-coord has the given Hamming weight"""
        bit_length = ZZ(curve.cardinality()).nbits()
        E = curve.ec()
        x_coord_count = 0
        x_coord = ZZ(2**params["weight"]-1)
        while True:
            if x_coord.nbits()>bit_length:
                break
            if E.is_x_coord(x_coord):
                x_coord_count+=1
            x_coord = next_hamming(x_coord)
        expected = binomial(bit_length, params["weight"]) // 2
        ratio = expected / x_coord_count
        curve_results = {
            "x_coord_count": x_coord_count,
            "expected": expected,
            "ratio": round(ratio, FLOAT_PRECISION),
        }
        return curve_results
