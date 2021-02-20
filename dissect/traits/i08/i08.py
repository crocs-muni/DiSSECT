#!/usr/bin/env python3

from sage.all import ZZ, GF

from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve


def i08_curve_function(curve: CustomCurve, k):
    """Computes the bit length of the x-coordinate of the generator multiplied by 1/k"""
    G = curve.generator
    if G is None:
        return {"Hx": None, "bits": None, "difference": None, "ratio": None}
    F = GF(curve.order)
    multiple = F(1) / k
    try:
        if k == 2:
            assert ZZ(multiple) == ZZ((curve.order + 1) / 2)
    except AssertionError:
        print(curve.order, ZZ(multiple), ZZ((curve.order + 1) / 2))
    H = ZZ(multiple) * G
    Hx = ZZ(H[0])
    bits = Hx.nbits()
    difference = ZZ(curve.cardinality).nbits() - bits
    ratio = bits / curve.nbits
    curve_results = {"Hx": Hx, "bits": bits, "difference": difference, "ratio": ratio}
    return curve_results


def compute_i08_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'i08', i08_curve_function, desc=desc, verbose=verbose)
