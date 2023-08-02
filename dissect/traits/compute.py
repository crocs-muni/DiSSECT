import argparse
import json
import sys

from dissect.traits import TRAITS
from dissect.utils.custom_curve import CustomCurve
from dissect.utils.database_handler import _cast_sage_types


def main():
    parser = argparse.ArgumentParser(description="DiSSECT trait computation script.")
    parser.add_argument(
        "-t",
        "--trait",
        type=str,
        choices=list(TRAITS.keys()),
        help="Trait identifier",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input curves file (stdin by default)",
        default=None,
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output file (stdout by default)", default=None
    )

    args = parser.parse_args()
    if args.trait not in TRAITS:
        print(f"Trait {args.trait} is not implemented", file=sys.stderr)
        sys.exit(1)

    results = {"data": []}
    if args.input:
        with open(args.input, "r") as f:
            curves = json.load(f)
    else:
        curves = json.load(sys.stdin)

    if not isinstance(curves, list):
        curves = curves["curves"]

    for curve in curves:
        curve = CustomCurve(curve)
        for params in TRAITS[args.trait].params_iter():
            result = {"curve": curve.name()}
            result["params"] = params
            result["result"] = TRAITS[args.trait](curve, **params)
            results["data"].append(result)

    json.dump(
        _cast_sage_types(results),
        sys.stdout if not args.output else open(args.output, "w"),
    )


if __name__ == "__main__":
    main()
