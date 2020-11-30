from sage.all import PolynomialRing, NumberField, ZZ

from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


# Computes the class number of the maximal order of the endomorphism algebra
# Time consuming
def a08_curve_function(curve):
    q = curve.q
    trace = curve.trace
    Q = PolynomialRing(ZZ, 'x')
    x = Q.gen()
    f = x ** 2 - trace * x + q
    K = NumberField(f, 'c')
    # G = K.class_group()
    h = K.class_number()
    curve_results = {"class_number": h}
    return curve_results


def compute_a08_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a08', a08_curve_function, desc=desc, verbose=verbose)


def get_a08_captions(results):
    return ["class_number"]


def select_a08_results(curve_results):
    keys = ["class_number"]
    selected_results = []
    for key in keys:
        selected_key = []
        for x in curve_results:
            selected_key.append(x[key])
        selected_results.append(selected_key)
    return selected_results


def pretty_print_a08_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a08', get_a08_captions, select_a08_results, save_to_txt=save_to_txt)
