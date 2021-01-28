from sage.all import factor

from curve_analyzer.traits.trait_interface import compute_results


def a22_curve_function(curve, l):
    """
    Computation factorization of l-th division polynomial
    Returns a dictionary (keys: 'factorization', 'degs_list', 'len' )
    """
    pol = curve.EC.division_polynomial(l)
    fact = [list(i) for i in list(factor(pol))]
    # count multiplicities?
    degs = [x.degree() for x, _ in fact]
    fact_str = [[str(i[0]), i[1]] for i in fact]
    curve_results = {'factorization': fact_str, 'degs_list': degs, 'len': len(degs)}
    return curve_results


def compute_a22_results(curve_list, desc='', verbose=False):
    compute_results(curve_list, 'a22', a22_curve_function, desc=desc, verbose=verbose)
