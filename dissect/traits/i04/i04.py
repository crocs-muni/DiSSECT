#!/usr/bin/env python3

from sage.all import ZZ, Combinations

from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
from dissect.utils.json_handler import FLOAT_PRECISION


def i04_curve_function(curve: CustomCurve, weight):
    """Computes the number of curve points whose x--cord has the given Hamming weight"""
    bit_length = ZZ(curve.cardinality).nbits()
    E = curve.EC
    x_coord_count = 0
    combination_list = Combinations(range(bit_length), weight).list()
    for combination in combination_list:
        binary = "0" * bit_length
        for bit in combination:
            binary = binary[:bit] + "1" + binary[bit + 1:]
        x_coord = ZZ("0b" + binary)
        if E.is_x_coord(x_coord):
            x_coord_count += 1
    expected = len(combination_list) // 2
    ratio = expected / x_coord_count
    curve_results = {"x_coord_count": x_coord_count, "expected": expected, "ratio": round(ratio, FLOAT_PRECISION)}
    return curve_results


def compute_i04_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'i04', i04_curve_function, desc=desc, verbose=verbose)
