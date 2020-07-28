from sage.all import factor, prime_range
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results

# Computation factorization of l-th division polynomial
# Returns a dictionary (keys: 'factorization', 'degs_list', 'len' )
def a22_curve_function(curve, l):
    pol = curve.EC.division_polynomial(l)
    fact = list(factor(pol))
    # count multiplicities?
    degs = [x.degree() for x, _ in fact]
    curve_results = {'factorization': fact, 'degs_list': degs, 'len': len(degs)}
    return curve_results


def compute_a22_results(curve_list, desc=''):
    compute_results(curve_list, 'a22', a22_curve_function, desc=desc)


def get_a22_captions(results):
    return ['degs_lists', 'lens']


def select_a22_results(curve_results):
    degs_lists = [x['degs_list'] for x in curve_results]
    lens = [x['len'] for x in curve_results]
    selected_results = [degs_lists, lens]
    return selected_results


def pretty_print_a22_results(curve_list, save_to_txt=True):
    pretty_print_results(curve_list, 'a22', get_a22_captions, select_a22_results, save_to_txt=save_to_txt)
