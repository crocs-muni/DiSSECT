from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
from dissect.traits.s02.pollard_functions import pollard


def s07_curve_function(curve: CustomCurve, weight):
    return pollard(curve, weight, 6, 2 ** 3)


def compute_s07_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "s07", s07_curve_function, desc=desc, verbose=verbose)
