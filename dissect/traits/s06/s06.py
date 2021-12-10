from dissect.traits.trait_interface import compute_results
from dissect.utils.custom_curve import CustomCurve
from dissect.traits.s02.pollard_functions import pollard


def s06_curve_function(curve: CustomCurve, weight):
    return pollard(curve, weight, 5, 2 ** 3)


def compute_s06_results(curve_list, desc="", verbose=False):
    compute_results(curve_list, "s06", s06_curve_function, desc=desc, verbose=verbose)
