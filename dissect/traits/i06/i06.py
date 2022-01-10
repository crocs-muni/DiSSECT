from dissect.utils.utils import Factorization
from dissect.utils.custom_curve import CustomCurve

TRAIT_TIMEOUT = 30


def i06_curve_function(curve: CustomCurve):
    """"Computes the square root of the square part of 4*p-1 and 4*generator_order-1 """
    order = curve.order()
    q = curve.q()
    curve_results = {"p": Factorization(4 * q - 1, use_ecm=False, timeout_duration=TRAIT_TIMEOUT).square_root(),
        "order": Factorization(4 * order - 1, use_ecm=False, timeout_duration=TRAIT_TIMEOUT).square_root()}
    return curve_results
