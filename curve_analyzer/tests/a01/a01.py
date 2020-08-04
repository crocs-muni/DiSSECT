from sage.all import GF, elliptic_curves
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results

def a01_curve_function(curve, deg):
    '''returns the orders of the two generators of the curve over the deg-th relative extension'''
    E = curve.EC
    q = curve.q
    curve_results = {}

    E_ext = E.base_extend(GF(q ** deg))
    curve_results['ord1'] = E_ext.abelian_group().gens()[0].order()
    if len(E_ext.gens()) < 2:
        curve_results['ord2'] = 1
    else:
        curve_results['ord2'] = E_ext.abelian_group().gens()[1].order()
    return curve_results


def compute_a01_results(curve_list, desc=''):
    compute_results(curve_list, 'a01', a01_curve_function, desc=desc)

def get_a01_captions(results):
    # TO DO
    pass

def select_a01_results(curve_results):
    # TO DO
    pass

def pretty_print_a01_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a01', get_a01_captions, select_a01_results, save_to_txt=save_to_txt)
