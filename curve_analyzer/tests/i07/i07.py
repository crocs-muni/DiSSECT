from sage.all import log, floor

from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


# Computes the distance of curve order to the nearest power of 2
def i07_curve_function(curve):
    order = curve.order * curve.cofactor
    l = floor(log(order, 2))
    u = l + 1
    L = 2 ** l
    U = 2 ** u
    curve_results = {"distance": U - order}
    if U - order > order - L:
        curve_results["distance"] = order - L
    return curve_results


def compute_i07_results(curve_list, desc=''):
    compute_results(curve_list, 'i07', i07_curve_function, desc=desc)


def get_i07_captions(results):
    return ["distance"]


def select_i07_results(curve_results):
    keys = ["distance"]
    selected_results = []
    for key in keys:
        selected_key = []
        for x in curve_results:
            selected_key.append(x[key])
        selected_results.append(selected_key)
    return selected_results


def pretty_print_i07_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'i07', get_i07_captions, select_i07_results, save_to_txt=save_to_txt)
