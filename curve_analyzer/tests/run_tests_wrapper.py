#!/usr/bin/env sage

# A wrapper for running individual tests from the command line.

import argparse
import sys

from curve_analyzer.utils.curve_handler import import_curves

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Welcome to Curve analyzer! It allows you to run tests on a selected subset of standard or simulated curves.')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-n', '--test_name', metavar='test_name', type=str, action='store',
                               help='the test identifier, e.g., a02', required=True)
    requiredNamed.add_argument('-c', '--curve_type', metavar='curve_type', type=str,
                               help='the type of curves to be tested; must be one of the following: std (all standard curves), sim (all simulated curves), sample (curves secp112r1, secp192r1, secp256r1), all (all curves in the database)',
                               required=True)
    parser.add_argument('-v', '--verbosity', action='store_true', help='verbosity flag (default: False)')
    parser.add_argument('-b', '--order_bound', action='store', type=int, metavar='order_bound', default=256,
                        help='upper bound for curve order bitsize (default: 256)')
    parser.add_argument('-d', '--description', action='store', type=str, metavar='description', default="",
                        help='custom text description of the current test run for logs (default: "")')
    parser.add_argument('--chunks_total', action='store', type=int, metavar='chunks_total', default=1,
                        help='the number of chunks into which the curve list is divided (default: 1)')
    parser.add_argument('--chunk', action='store', type=int, metavar='chunk', default=1,
                        help='the chunk of the curve list that will be processed (default: 1)')

    args = parser.parse_args()
    tn = args.test_name
    module_name = tn + '.' + tn
    try:
        __import__(module_name)
    except ModuleNotFoundError:
        print("please enter a valid test identifier, e.g., a02")
        exit()
    test_function = getattr(sys.modules[module_name], "compute_" + tn + "_results")

    ctype = args.curve_type
    if not ctype in ["std", "sim", "sample", "all"]:
        print("curve_type must be one of std, sim, sample, all")
        exit()

    curves_list = import_curves(curve_type=args.curve_type, order_bound=args.order_bound, verbose=args.verbosity,
                                chunks_total=args.chunks_total, chunk=args.chunk)
    print("")
    test_function(curves_list, desc=args.description)
