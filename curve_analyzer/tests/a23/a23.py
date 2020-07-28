from sage.all import kronecker, ZZ, prime_range
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results


# Computes the depth of volcano and the degree of the crater subgraph containing E
# Returns a dictionary (keys: 'crater_degree', 'depth')
def a23_curve_function(curve, l):
    E = curve.EC
    t = curve.trace
    q = curve.q
    curve_results = {}
    D = t ** 2 - 4 * q
    if l != 2:
        curve_results['crater_degree'] = kronecker(D, l) + 1
        curve_results['depth'] = ZZ.valuation(l)(D) // 2
    else:
        e = ZZ.valuation(2)(D)
        if e % 2 == 0:
            d = D // (2 ** e)
            if d % 4 != 1:
                curve_results['crater_degree'] = 1
                curve_results['depth'] = e // 2 - 1
            else:
                curve_results['crater_degree'] = kronecker(d, l) + 1
                curve_results['depth'] = e // 2
        else:
            curve_results['crater_degree'] = 1
            curve_results['depth'] = e // 2 - 1
    return curve_results


def compute_a23_results(curve_list, desc=''):
    compute_results(curve_list, 'a23', a23_curve_function, desc=desc)


def get_a23_captions(results):
    captions = ['crater_degree', 'depth']
    return captions


def select_a23_results(curve_results):
    degs_lists = [x['crater_degree'] for x in curve_results]
    depths = [x['depth'] for x in curve_results]
    selected_results = [degs_lists, depths]
    return selected_results


def pretty_print_a23_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a23', get_a23_captions, select_a23_results, save_to_txt=save_to_txt)
