from sage.all import GF

from curve_analyzer.tests.test_interface import pretty_print_results, compute_results, timeout

# global time for one factorization
TIME = 10



def a01_curve_function(curve, deg):
    '''returns the orders of the two generators of the curve over the deg-th relative extension'''
    E = curve.EC
    q = curve.q
    curve_results = {}

    E_ext = E.base_extend(GF(q ** deg))
    t = TIME
    try:
        gens = [timeout(E_ext.abelian_group().gens()[0].order, [], timeout_duration=t)]
    except:
        return None
    try:
        gens.append(timeout(E_ext.abelian_group().gens()[1].order, [], timeout_duration=t))
    except:
        pass
    curve_results['ord1'] = gens[0]
    if len(gens) < 2:
        curve_results['ord2'] = 1
    else:
        curve_results['ord2'] = gens[1]
    return curve_results


def compute_a01_results(curve_list, desc=''):
    compute_results(curve_list, 'a01', a01_curve_function, desc=desc)


def get_a01_captions(results):
    return ['ord1', 'ord2']


def select_a01_results(curve_results):
    keys = ['ord1', 'ord2']
    selected_results = []
    for key in keys:
        for x in curve_results:
            selected_results.append(x[key])
    return selected_results


def pretty_print_a01_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a01', get_a01_captions, select_a01_results, save_to_txt=save_to_txt)
