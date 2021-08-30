#!/usr/bin/env python3

from sage.all import ZZ, binomial

from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
from dissect.utils.json_handler import FLOAT_PRECISION

def next_hamming(val):
    c = val & -val
    r = val + c
    return ZZ((((r ^ val) >> 2) // c) | r)

def i04_curve_function(curve: CustomCurve, weight):
    """Computes the number of curve points whose x-coord has the given Hamming weight"""
    bit_length = ZZ(curve.cardinality()).nbits()
    E = curve.ec()
    x_coord_count = 0
    x_coord = ZZ(2**weight-1)
    while True:
        if x_coord.nbits()>bit_length:
            break
        if E.is_x_coord(x_coord):
            x_coord_count+=1
        x_coord = next_hamming(x_coord)
    expected = binomial(bit_length,weight) // 2
    ratio = expected / x_coord_count
    curve_results = {
        "x_coord_count": x_coord_count,
        "expected": expected,
        "ratio": round(ratio, FLOAT_PRECISION),
    }
    return curve_results


def compute_i04_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "i04", i04_curve_function, desc=desc, verbose=verbose)
