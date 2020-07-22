from sage.all_cmdline import *   # import sage library
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results

def a22_curve_function(curve, l):
    pol = curve.EC.division_polynomial(l)
    fact = list(factor(pol))
    # count multiplicities?
    degs = [x.degree() for x, _ in fact]
    curve_results = {'factorization': fact, 'degs_list': degs, 'len': len(degs)}
    return curve_results

def compute_a22_results(curve_list, l_max = 20, order_bound = 256, overwrite = False, desc = ''):
    global_params = {'l_range': prime_range(l_max)}
    params_local_names = ['l']
    #Add Ordered dict
    compute_results(curve_list,'a22', a22_curve_function, global_params, params_local_names, order_bound, overwrite, desc = desc)

def get_a22_captions(results):
    captions = ['degs_lists', 'lens']
    return captions

def select_a22_results(curve_results):
    degs_lists = [x['degs_list'] for x in curve_results]
    lens = [x['len'] for x in curve_results]
    selected_results = [degs_lists, lens]
    return selected_results

def pretty_print_a22_results(curve_list, save_to_txt = True):
    pretty_print_results('a22', get_a22_captions, select_a22_results, save_to_txt = save_to_txt, curve_list = curve_list)
