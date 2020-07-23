from sage.all import kronecker, ZZ
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


def compute_a23_results(order_bound=256, overwrite=False, curve_list=None):
    if curve_list == None:
        from curve_analyzer.utils.curve_handler import curves
        curve_list = curves
    parameters = {}
    compute_results(curve_list, 'a23', a23_curve_function, parameters, order_bound, overwrite)


def pretty_print_a23_results(save_to_txt=True, curve_list=None):
    if curve_list == None:
        from curve_analyzer.utils.curve_handler import curves
        curve_list = curves
    pretty_print_results(curve_list, 'a23', [['crater_degree'], ['depth']], ['crater_degree', 'depth'],
                         save_to_txt=save_to_txt)
