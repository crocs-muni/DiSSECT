from sage.all_cmdline import *   # import sage library
from curve_analyzer.tests.test_interface import pretty_print_results, compute_results

# Computation of number of prime degree divisors of trace
# Returns a dictionary (key: 'trace') 
def a25_curve_function(curve):
    return {'trace':len(list(factor(curve.trace)))}

def compute_a25_results(curve_list, order_bound = 256 , overwrite = False):
    parameters = {}
    compute_results('a25', a25_curve_function, parameters, order_bound, overwrite)

def pretty_print_a25_results(curve_list, save_to_txt = True):
    pretty_print_results('a25', [['trace']], ['trace factorization'], save_to_txt = save_to_txt, curve_list = curve_list)
   

