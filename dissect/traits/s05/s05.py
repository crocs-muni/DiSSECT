from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
from dissect.traits.s02.pollard_functions import pollard


def s05_curve_function(curve: CustomCurve, weight):
    return pollard(curve, weight, 4, 2 ** 3)


def compute_s05_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "s05", s05_curve_function, desc=desc, verbose=verbose)
