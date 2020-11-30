from sage.all import floor

from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


# Computes the distance of curve order to the nearest power of 2 and to the nearest multiple of 32 and 64
def i07_curve_function(curve):
    order = curve.order * curve.cofactor
    l = order.nbits() - 1
    u = l + 1
    L = 2 ** l
    U = 2 ** u
    distance = min(order - L, U - order)
    dist32 = min(abs(order % 32), 32 - abs(order % 32))
    dist64 = min(abs(order % 64), 64 - abs(order % 64))
    ratio = floor(order / distance)
    curve_results = {"distance": distance, "ratio": ratio, "distance 32": dist32, "distance 64": dist64}
    return curve_results


def compute_i07_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'i07', i07_curve_function, desc=desc, verbose=verbose)


def get_i07_captions(curve_results):
    return ["distance", "ratio", "distance 32", "distance 64"]


def select_i07_results(curve_results):
    keys = ["distance", "ratio", "distance 32", "distance 64"]
    selected_results = []
    for key in keys:
        selected_key = []
        for x in curve_results:
            selected_key.append(x[key])
        selected_results.append(selected_key)
    return selected_results


def pretty_print_i07_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'i07', get_i07_captions, select_i07_results, save_to_txt=save_to_txt)
