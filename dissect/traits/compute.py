#!/usr/bin/env python3

import argparse
import json
import sys

from dissect.utils.custom_curve import CustomCurve

from dissect.utils.database_handler import _cast_sage_types
from dissect.definitions import TRAIT_NAMES, TRAIT_MODULE_PATH
from dissect.traits.trait_info import params_iter


def get_trait_function(trait):
    module_name = TRAIT_MODULE_PATH + "." + trait + "." + trait
    try:
        __import__(module_name)
    except ModuleNotFoundError:
        return None
    return getattr(sys.modules[module_name], trait + "_curve_function")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DiSSECT trait computation script."
    )
    parser.add_argument(
        "-t",
        "--trait",
        type=str,
        choices=TRAIT_NAMES,
        help="Trait identifier",
        required=True
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input file (JSON of curves)",
        required=True
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file (stdout by default)",
        default=None
    )

    args = parser.parse_args()
    trait_function = get_trait_function(args.trait)
    if not trait_function:
        print(f"Trait could not be loaded", file=sys.stderr)
        sys.exit(1)

    results = { "data": [] }
    with open(args.input, "r") as f:
        curves = json.load(f)
        if not isinstance(curves, list):
            curves = curves["curves"]

    for curve in curves:
        curve = CustomCurve(curve)
        for params in params_iter(args.trait):
            result = { "curve": curve.name() }
            result["params"] = params
            result["result"] = trait_function(curve, **params)
            results["data"].append(result)

    json.dump(_cast_sage_types(results), sys.stdout if not args.output else open(args.output, "w"))
