import dissect.traits.trait_utils as tu
from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve

TRAIT_TIMEOUT = 30


def i06_curve_function(curve: CustomCurve):
    """"Computes the square root of the square part of 4*p-1 and 4*generator_order-1 """
    order = curve.order
    q = curve.q
    curve_results = {
        "p": tu.square_part_square_root(4 * q - 1, use_ecm=False),
        "order": tu.square_part_square_root(4 * order - 1, use_ecm=False),
    }
    return curve_results


def compute_i06_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "i06", i06_curve_function, desc=desc, verbose=verbose)
