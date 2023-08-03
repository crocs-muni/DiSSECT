#!/usr/bin/env python3

from time import sleep
import sys

import pandas as pd
import argparse

from dissect.traits import TRAITS
import dissect.analysis.data_processing as dp


def main():
    parser = argparse.ArgumentParser(
        description="Welcome to DiSSECT feature vector builder! It allows you to join trait results into vectors suitable for further analysis."
    )
    parser.add_argument(
        "-t",
        "--trait",
        type=str,
        help="trait name",
        required=True,
    )
    parser.add_argument(
        "--category",
        nargs="+",
        type=str,
        default="all",
        help="category of applicable curves",
    )
    parser.add_argument(
        "--bits",
        nargs="+",
        type=str,
        default="all",
        help="bitlength of applicable curves",
    )
    parser.add_argument(
        "--cofactors",
        nargs="+",
        type=str,
        default="all",
        help="the list of cofactors the curve can have (default: all)",
    )
    parser.add_argument(
        "--output", type=str, default=None, help="output file (default stdout)"
    )
    parser.add_argument(
        "--input", type=str, default=None, help="input file (default stdin)"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="https://dissect.crocs.fi.muni.cz/",
        help="data source",
    )
    parser.add_argument(
        "--example", type=str, default=None, help="example curves (default: all)"
    )
    parser.add_argument(
        "--keep-category",
        action="store_true",
        default=False,
        help="keep category in the resulting csv",
    )

    args = vars(parser.parse_args())
    input = args["input"]
    del args["input"]
    source = args["source"]
    del args["source"]
    output = args["output"]
    del args["output"]
    trait = args["trait"]
    del args["trait"]
    keep_columns = ["curve", "category"] if args["keep_category"] else ["curve"]
    del args["keep_category"]

    try:
        curves = pd.read_csv(
            input if input else sys.stdin, sep=";", index_col=False, low_memory=False
        )
    except FileNotFoundError:
        curves = dp.get_curves(source, args)[keep_columns]

    for i in range(3):
        try:
            trait_df = dp.get_trait(source, trait, args, False)
            break
        except:
            print(f"Reconnecting attempt {i} ...")
            sleep(10)

    for feature in TRAITS[trait].numeric_outputs():
        dp.clean_feature(trait_df, feature)

    flat_df = dp.flatten_trait(trait, trait_df)
    features = list(filter(lambda x: x not in keep_columns, flat_df.columns))

    for feature in features:
        dp.scale_feature(flat_df, feature)

    curves = curves.merge(flat_df, "left", on="curve")

    for feature in features:
        dp.impute_feature(curves, feature, -1.0)

    curves.to_csv(output if output else sys.stdout, sep=";", index=False)


if __name__ == "__main__":
    main()
