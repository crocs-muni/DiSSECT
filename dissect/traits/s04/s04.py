from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
from dissect.traits.s02.pollard_functions import pollard


def s04_curve_function(curve: CustomCurve, weight):
    return pollard(curve, weight, 3, 2 ** 6)


def compute_s04_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "s04", s04_curve_function, desc=desc, verbose=verbose)
