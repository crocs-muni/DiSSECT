#!/usr/bin/env python3

# A wrapper for running individual traits from the command line.

import argparse
import sys

from dissect.definitions import TRAIT_NAMES, TRAIT_MODULE_PATH
from dissect.utils.curve_handler import import_curves


def main():
    parser = argparse.ArgumentParser(
        description="Welcome to Curve analyzer! It allows you to run traits on a selected subset of standard or "
        "simulated curves."
    )
    requiredNamed = parser.add_argument_group("required named arguments")
    requiredNamed.add_argument(
        "-n",
        "--trait_name",
        metavar="trait_name",
        type=str,
        action="store",
        help="the trait identifier; available traits: " + ", ".join(TRAIT_NAMES),
        required=True,
    )
    requiredNamed.add_argument(
        "-c",
        "--curve_type",
        metavar="curve_type",
        type=str,
        help="the type of curves or which to compute traits; must be one of the following: std (all standard "
        "curves), sim (all simulated curves), sample (curves secp112r1, secp192r1, "
        "secp256r1), all (all curves in the database)",
        required=True,
    )
    parser.add_argument(
        "-v", "--verbosity", action="store_true", help="verbosity flag (default: False)"
    )
    parser.add_argument(
        "-b",
        "--order_bound",
        action="store",
        type=int,
        metavar="order_bound",
        default=256,
        help="upper bound for curve order bitsize (default: 256)",
    )
    parser.add_argument(
        "-d",
        "--description",
        action="store",
        type=str,
        metavar="description",
        default="",
        help='custom text description of the current trait run for logs (default: "")',
    )
    parser.add_argument(
        "-a",
        "--allowed_cofactors",
        nargs="+",
        metavar="allowed_cofactors",
        default=[1],
        help="the list of cofactors the curve can have (default: [1])",
    )
    parser.add_argument(
        "--chunks_total",
        action="store",
        type=int,
        metavar="chunks_total",
        default=1,
        help="the number of chunks into which the curve list is divided (default: 1)",
    )
    parser.add_argument(
        "--chunk",
        action="store",
        type=int,
        metavar="chunk",
        default=1,
        help="the chunk of the curve list that will be processed (default: 1)",
    )

    args = parser.parse_args()
    tn = args.trait_name
    module_name = TRAIT_MODULE_PATH + "." + tn + "." + tn
    try:
        __import__(module_name)
    except ModuleNotFoundError:
        print("please enter a valid trait identifier, e.g., a02")
        exit()
    trait_function = getattr(sys.modules[module_name], "compute_" + tn + "_results")
    ctype = args.curve_type
    if ctype not in ["std", "sim", "sample", "all"]:
        print("curve_type must be one of std, sim, sample, all")
        exit()
    curves_list = import_curves(
        curve_type=args.curve_type,
        order_bound=args.order_bound,
        verbose=args.verbosity,
        allowed_cofactors=args.allowed_cofactors,
        chunks_total=args.chunks_total,
        chunk=args.chunk,
    )
    trait_function(curves_list, desc=args.description, verbose=args.verbosity)


if __name__ == "__main__":
    main()
