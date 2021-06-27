#!/usr/bin/env python3

import pathlib
import json
import itertools
import pandas as pd
import argparse

from sage.all import sage_eval

from dissect.definitions import TRAIT_NAMES, TRAIT_PATH
from dissect.traits.trait_info import TRAIT_INFO
import dissect.analysis.data_processing as dp

def params_range(trait_name):
    with open(pathlib.Path(TRAIT_PATH, trait_name, trait_name + ".params"), "r") as params_file:
        params = json.load(params_file)

    params_names = params["params_local_names"]
    params_ranges = {}
    for key in params["params_global"].keys():
        params_ranges[key] = sage_eval(params["params_global"][key])

    for params_values in itertools.product(*params_ranges.values()):
        yield dict(zip(params_names, params_values))


def numeric_outputs(trait_name):
    outputs = []

    for output, info in TRAIT_INFO[trait_name]["output"].items():
        if info[0] == int or info[0] == float:
            outputs.append(output)

    return outputs

def main(source, trait_name, bitlength=0, cofactor=0, output="print"):
    curves = dp.load_curves(source)
    trait = dp.load_trait(source, trait_name)
    trait = curves.merge(trait, "inner", on="curve")

    if bitlength:
        trait = trait[trait["bitlength"] == bitlength]
    if cofactor:
        trait = trait[trait["cofactor"] == cofactor]
    trait.reset_index(inplace=True, drop=True)

    features = numeric_outputs(trait_name)

    outlier_df = pd.DataFrame()

    for params in params_range(trait_name):
        t = trait
        for param in params:
            t = t[t[param] == params[param]]
        outliers = dp.find_outliers(t, features)
        outlier_df = pd.concat([outlier_df, outliers], ignore_index=True)
        outliers = outliers["curve"].tolist()
        if output == "print":
            if len(outliers) > 0:
                print(f"Outliers for {trait_name}: {params}")
                print("  " + "\n  ".join(outliers))
            else:
                print(f"No outliers found for {trait_name}: {params}.")

    if output == "csv":
        print(outlier_df.to_csv(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DiSSECT Outlier Detection")
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
    parser.add_argument(
        "--bitlength",
        action="store",
        type=int,
        default=0,
        help="bitlength of analyzed curves (default: all)",
    )
    parser.add_argument(
        "--cofactor",
        type=int,
        metavar="cofactor",
        default=0,
        help="cofactor of the analyzed curves (default: all)",
    )
    parser.add_argument(
        "--source",
        type=str,
        default="https://dissect.crocs.fi.muni.cz/static/data/",
        help="Data source URI (default: https://dissect.crocs.fi.muni.cz/static/data/",
    )
    parser.add_argument('--csv', action='store_const', const="csv")

    args = parser.parse_args()

    output = "print" if not args.csv else "csv"
    main(args.source, args.trait_name, args.bitlength, args.cofactor, output)
