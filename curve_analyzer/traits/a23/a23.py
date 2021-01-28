from sage.all import kronecker, ZZ

from curve_analyzer.traits.trait_interface import compute_results


def a23_curve_function(curve, l):
    '''
    Computes the depth of volcano and the degree of the crater subgraph containing E
    Returns a dictionary (keys: 'crater_degree', 'depth')
    '''
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


def compute_a23_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a23', a23_curve_function, desc=desc, verbose=verbose)
