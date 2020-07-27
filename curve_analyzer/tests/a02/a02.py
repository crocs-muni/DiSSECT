from sage.all import ZZ, sqrt, factor, squarefree_part
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


# Computation of d_K (cm_disc), v (max_conductor) and factorization of D where D=t^2-4q = v^2*d_K
# Returns a dictionary (keys: 'cm_disc', 'factorization', 'max_conductor') 
def a02_curve_function(curve):
    E = curve.EC
    t = curve.trace
    q = curve.q
    curve_results = {}
    D = t ** 2 - 4 * q
    d = squarefree_part(D)
    disc = d
    if d % 4 != 1:
        disc *= 4
    curve_results['cm_disc'] = disc
    curve_results['factorization'] = list(factor(D))
    curve_results['max_conductor'] = ZZ(sqrt(D / disc))
    return curve_results


def compute_a02_results(curve_list, order_bound=256, overwrite=False, desc=''):
    global_params = {}
    params_local_names = []
    compute_results(curve_list, 'a02', a02_curve_function, global_params, params_local_names, order_bound, overwrite,
                    desc=desc)


def get_a02_captions(results):
    return ['max_conductor', 'factorization', 'cm_disc']


def select_a02_results(curve_results):
    selected_results = []
    for key in curve_results.keys():
        selected_results.append(curve_results[key])
    return selected_results


def pretty_print_a02_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a02', get_a02_captions, select_a02_results, save_to_txt=save_to_txt)
