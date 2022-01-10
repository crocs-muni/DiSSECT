#!/usr/bin/env python3
from dissect.utils.utils import Factorization
from dissect.utils.custom_curve import CustomCurve

TRAIT_TIMEOUT = 30


def a03_curve_function(curve: CustomCurve, deg):
    """Returns the factorization of the cardinality of the quadratic twist of the curve"""
    tr = curve.extended_trace(deg)
    card = curve.extended_cardinality(deg)
    twist_card = card + 2 * tr
    f = Factorization(twist_card, timeout_duration=TRAIT_TIMEOUT)

    curve_results = {"twist_cardinality": twist_card, "factorization": f.factorization()}
    return curve_results
