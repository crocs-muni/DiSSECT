from sage.all import factor
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


# Computation of number of prime degree divisors of trace
# Returns a dictionary (key: 'trace') 
def a25_curve_function(curve):
    return {'trace': len(list(factor(curve.trace)))}


def compute_a25_results(curve_list, order_bound=256, overwrite=False, desc=''):
    global_params = {}
    params_local_names = []
    compute_results(curve_list, 'a25', a25_curve_function, global_params, params_local_names, order_bound, overwrite,
                    desc=desc)


def get_a25_captions(results):
    captions = ['trace']
    return captions


def select_a25_results(curve_results):
    keys = ['trace']
    selected_results = []
    for key in keys:
        for x in curve_results:
            selected_results.append(x[key])
    return selected_results


def pretty_print_a25_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a25', get_a25_captions, select_a25_results, save_to_txt=save_to_txt)
