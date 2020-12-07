from sage.all import squarefree_part, sqrt

from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


def i06_curve_function(curve):
    '''Computes the square part of 4*p-1. 4*order-1 (result is square root of the square part)'''
    order = curve.order  # * curve.cofactor
    q = curve.q
    a = 4 * q - 1
    b = 4 * order - 1
    curve_results = {"p": sqrt(a // squarefree_part(a)), "order": sqrt(b // squarefree_part(b))}
    return curve_results


def compute_i06_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'i06', i06_curve_function, desc=desc, verbose=verbose)


def get_i06_captions(curve_results):
    return ["p", "order"]


def select_i06_results(curve_results):
    keys = ["p", "order"]
    selected_results = []
    for key in keys:
        selected_key = []
        for x in curve_results:
            selected_key.append(x[key])
        selected_results.append(selected_key)
    return selected_results


def pretty_print_i06_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'i06', get_i06_captions, select_i06_results, save_to_txt=save_to_txt)
