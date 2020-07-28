#!/usr/bin/env sage

import argparse
import sys
from curve_analyzer.utils.curve_handler import import_curves

parser = argparse.ArgumentParser(description='Welcome to Curve analyzer! It allows you to run tests on a selected subset of standard or simulated curves.')
parser.add_argument('test_name', metavar='test_name', type=str, nargs=1, action='store', help='the test identifier, e.g., a02')
parser.add_argument('curve_type', metavar='curve_type', type=str, nargs=1, help='the type of curves to be tested; must be one of the following: std (all standard curves), sim (all simulated curves), sample (curves secp112r1, secp192r1, secp256r1), all (all curves in the database)')
parser.add_argument('-v', '--verbosity', action='store_true', help='verbosity flag (default: False)')
parser.add_argument('-b', action='store', type=int, metavar='order_bound', help ='upper bound for curve order bitsize (default: 256)')

args = parser.parse_args()
tn = args.test_name[0]
module_name = tn + '.' + tn
try:
    __import__(module_name)
except ModuleNotFoundError:
    print("please enter a valid test identifier, e.g., a02")
    exit()
test_function = getattr(sys.modules[module_name], "compute_" + tn + "_results")

ct = args.curve_type[0]
if not ct in ["std", "sim", "sample", "all"]:
    print("curve_type must be one of std, sim, sample, all")
    exit()

if args.b == None:
	order_bound = 256
else:
	order_bound = args.b
curves_list = import_curves(ct, order_bound, args.verbosity)
print("")
test_function(curves_list)