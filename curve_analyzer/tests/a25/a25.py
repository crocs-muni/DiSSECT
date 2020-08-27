from sage.all import factor

from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


# Computation of number of prime degree divisors of trace
# Returns a dictionary (key: 'trace') 
def a25_curve_function(curve):
    f = list(factor(curve.trace))
    curve_results = {'trace_factorization': f, 'number_of_factors': len(f)}
    return curve_results


def compute_a25_results(curve_list, desc=''):
    compute_results(curve_list, 'a25', a25_curve_function, desc=desc)


def get_a25_captions(results):
    captions = ['trace']
    return captions


def select_a25_results(curve_results):
    keys = ['trace']
    selected_results = []
    for key in keys:
        selected_key = []
        for x in curve_results:
            selected_key.append(x[key])
        selected_results.append(selected_key)
    return selected_results


def pretty_print_a25_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a25', get_a25_captions, select_a25_results, save_to_txt=save_to_txt)
