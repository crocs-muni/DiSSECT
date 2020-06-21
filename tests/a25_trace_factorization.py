from sage.all_cmdline import *   # import sage library
from curve_analyzer.tests.curve_handler import curves
import curve_analyzer.tests.test_interface

# Computation of number of prime degree divisors of trace
# Returns a dictionary (key: 'trace') 
def a25_curve_function(curve):
    return {'trace':len(list(factor(curve.trace)))}

def compute_a25_results(order_bound = 256 , overwrite = False, curve_list = curves):
    parameters = {}
    compute_results('a25', a25_curve_function, parameters, order_bound, overwrite, curve_list = curve_list)

def pretty_print_a25_results(save_to_txt = True):
    pretty_print_results('a25', [['trace']], ['trace factorization'], save_to_txt = save_to_txt)
   

