#!/usr/bin/env python3

from time import sleep

import pandas as pd
from decimal import Decimal
import argparse

from dissect.definitions import TRAIT_PATH
from dissect.traits.trait_info import TRAIT_INFO, numeric_outputs, nonnumeric_outputs
import dissect.analysis.data_processing as dp

def clean_feature(df, feature):
    def cleaner(value):
        if value in ("NO DATA (timed out)", "INVALID DATA Ran out of input", "-", None):
            return pd.NA
        return Decimal(value)

    df[feature] = df[feature].map(cleaner, na_action="ignore")


def scale_feature(df, feature):
    df[feature] = df[feature].map(Decimal, na_action="ignore")
    feature_max = df[feature].max(skipna=True)
    feature_min = df[feature].min(skipna=True)
    feature_range = feature_max - feature_min

    def scaler(x): # minmax
        if feature_range == Decimal(0):
            result = x / (Decimal(1) if feature_max == Decimal(0) else feature_max)
        else:
            result = (x - feature_min) / feature_range
        return result

    df[feature] = df[feature].map(scaler, na_action="ignore")
    df[feature] = df[feature].map(float, na_action="ignore")


def impute_feature(df, feature, method="mean"):
    if method == "mean":
        value = df[feature].mean(skipna=True)
    elif method == "median":
        value = df[feature].median(skipna=True)
    else:
        value = method

    df[feature] = df[feature].fillna(float(value))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Welcome to DiSSECT feature vector builder! It allows you to join trait results into vectors suitable for further analysis.")
    parser.add_argument(
        "-n",
        "--trait",
        type=str,
        help="trait name",
        required=True,
    )
    parser.add_argument(
        "--category",
        nargs="+",
        type=str,
        default=None,
        help="category of applicable curves"
    )
    parser.add_argument(
        "--bitlength",
        type=str,
        default="",
        help="bitlength of applicable curves (or a range X-Y)",
    )
    parser.add_argument(
        "--cofactors",
        nargs="+",
        type=int,
        default=None,
        help="the list of cofactors the curve can have (default: all)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="out.csv",
        help="output file name"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="out.csv",
        help="input file name"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="https://dissect.crocs.fi.muni.cz/static/data/",
        help="data source"
    )


    args = parser.parse_args()

    try:
        curves = pd.read_csv(args.input, sep=';', index_col=False, low_memory=False)
    except FileNotFoundError:
        curves = dp.load_curves(args.source)

        if hasattr(args, "category") and args.category:
            curves = curves[curves["category"].isin(args.category)]
        if hasattr(args, "bitlength") and args.bitlength:
            bitlength_range = list(map(int, args.bitlength.split("-")))
            if len(bitlength_range) == 2:
                curves = curves[(curves["bitlength"] >= bitlength_range[0]) & (curves["bitlength"] <= bitlength_range[1])]
            else:
                curves = curves[curves["bitlength"] == bitlength_range[0]]
        if hasattr(args, "cofactors") and args.cofactors:
            curves = curves[curves["cofactor"].isin(args.cofactors)]

        curves = curves[["curve"]]

    TRAIT_NAME = args.trait
    for i in range(3):
        try:
            trait_df = dp.load_trait(args.source, TRAIT_NAME)
            break
        except:
            print(f"Reconnecting attempt {i} ...")
            sleep(10)

    for feature in numeric_outputs(TRAIT_NAME):
        clean_feature(trait_df, feature)

    flat_df = dp.flatten_trait(TRAIT_NAME, trait_df)
    features = list(filter(lambda x: x != "curve", flat_df.columns))
    for feature in features:
        scale_feature(flat_df, feature)

    curves = curves.merge(flat_df, "left", on="curve")

    for feature in features:
        impute_feature(curves, feature, "mean")

    curves.to_csv(args.output, sep=';', index=False)