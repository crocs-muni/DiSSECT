#!/usr/bin/env sage

# A script for running individual tests from the command line.

import argparse
import sys

from curve_analyzer.utils.curve_handler import import_curves

parser = argparse.ArgumentParser(
    description='Welcome to Curve analyzer! It allows you to run tests on a selected subset of standard or simulated curves.')
parser.add_argument('test_name', metavar='test_name', type=str, nargs=1, action='store',
                    help='the test identifier, e.g., a02')
parser.add_argument('curve_type', metavar='curve_type', type=str, nargs=1,
                    help='the type of curves to be tested; must be one of the following: std (all standard curves), sim (all simulated curves), sample (curves secp112r1, secp192r1, secp256r1), all (all curves in the database)')
parser.add_argument('-v', '--verbosity', action='store_true', help='verbosity flag (default: False)')
parser.add_argument('-b', action='store', type=int, metavar='order_bound',
                    help='upper bound for curve order bitsize (default: 256)')
parser.add_argument('-d', action='store', type=str, metavar='description',
                    help='custom text description of the current test run for logs (default: "")')
parser.add_argument('-ct', action='store', type=int, metavar='chunks_total',
                    help='the number of chunks into which the curve list is divided (default: 1)')
parser.add_argument('-c', action='store', type=int, metavar='chunk',
                    help='the chunk of the curve list that will be processed (default: 1)')

args = parser.parse_args()
tn = args.test_name[0]
module_name = tn + '.' + tn
try:
    __import__(module_name)
except ModuleNotFoundError:
    print("please enter a valid test identifier, e.g., a02")
    exit()
test_function = getattr(sys.modules[module_name], "compute_" + tn + "_results")

ctype = args.curve_type[0]
if not ctype in ["std", "sim", "sample", "all"]:
    print("curve_type must be one of std, sim, sample, all")
    exit()

if args.b == None:
    order_bound = 256
else:
    order_bound = args.b

if args.d == None:
    description = ""
else:
    description = args.d

if args.ct == None:
    ct = 1
else:
    ct = args.ct

if args.c == None:
    c = 1
else:
    c = args.c

curves_list = import_curves(ctype, order_bound, args.verbosity, chunks_total=ct, chunk=c)
print("")
print(curves_list)
test_function(curves_list, desc=description)
