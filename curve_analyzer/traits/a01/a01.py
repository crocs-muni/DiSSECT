from sage.all import GF, ZZ

from curve_analyzer.traits.trait_interface import pretty_print_results, compute_results, timeout

# global time for one group computation
TIME = 100


def compute_second_generator_order(E_ext):
    '''compute the second group generator order only (if it exists), in order to have synergy with timeout'''
    gens = E_ext.abelian_group().gens()
    if len(gens) == 1:
        return 1
    else:
        return gens[1].order

def a01_curve_function(curve, deg):
    """returns the orders of the two generators of the curve over the deg-th relative extension"""
    curve_results = {}
    t = TIME
    E = curve.EC
    q = curve.q
    E_ext = E.base_extend(GF(q ** deg))
    curve_results['ord2'] = timeout(compute_second_generator_order, [E_ext], timeout_duration=t)
    if isinstance(curve_results['ord2'], int):
        curve_results['ord1'] = ZZ(E_ext.cardinality() / curve_results['ord2'])
    else:
        curve_results['ord1'] = None
    return curve_results


def compute_a01_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a01', a01_curve_function, desc=desc, verbose=verbose)


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
