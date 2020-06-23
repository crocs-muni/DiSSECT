from sage.all_cmdline import *   # import sage library

from curve_analyzer.utils.curve_handler import *
from curve_analyzer.tests.test_interface import *

def a22_curve_function(curve, l_max):
    E = curve.EC
    curve_results = {'degs_list': [], 'lens': []}

    for l in prime_range(l_max):
        pol = c.EC.division_polynomial(l)
        fact = list(factor(pol))
        degs = [x.degree() for x,_ in fact]
        curve_results['degs_list'].append(degs)
        curve_results['lens'].append(len(degs))
    return curve_results

def compute_a22_results(l_max = 20, order_bound = 256, overwrite = False, curve_list = curves):
    parameters = {'l_max': l_max}
    compute_results('a22', a22_curve_function, parameters, order_bound, overwrite, curve_list = curve_list)

def pretty_print_a22_results(save_to_txt = True):
    pretty_print_results('a22', [['lens']], ['Number of irreducible factors of l-th division polynomial'], save_to_txt = save_to_txt, res_sort_key = lambda x: 1 )

