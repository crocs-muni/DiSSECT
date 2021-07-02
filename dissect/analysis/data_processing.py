from typing import Dict, Any
import urllib.request
import json
import bz2
from sage.all import RR, ZZ

import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import MinMaxScaler

import dissect.utils.database_handler as database
from dissect.definitions import STD_CURVE_DICT, ALL_CURVE_COUNT
from dissect.traits.trait_info import TRAIT_INFO, params_iter, nonnumeric_outputs


class Modifier:
    """a class of lambda functions for easier modifications if visualised values"""

    def __init__(self):
        pass

    @staticmethod
    def identity():
        return lambda x: x

    @staticmethod
    def ratio(ratio_precision=3):
        return lambda x: RR(x).numerical_approx(digits=ratio_precision)

    @staticmethod
    def bits():
        return lambda x: ZZ(x).nbits()

    @staticmethod
    def factorization_bits(factor_index=-1):
        return lambda x: ZZ(x[factor_index]).nbits()

    @staticmethod
    def length():
        return lambda x: len(x)


def load_trait(source: str, trait: str, params: Dict[str, Any] = None, curve: str = None,
               skip_timeouts: bool = False) -> pd.DataFrame:
    if source.startswith("mongodb"):
        trait_results = database.get_trait_results(database.connect(source), trait)
    else:  # if source.startswith("http"):
        with urllib.request.urlopen(source + f"dissect.trait_{trait}.json.bz2") as f:
            trait_results = json.loads(bz2.decompress(f.read()).decode("utf-8"))
            trait_results = map(database._decode_ints, map(database._flatten_trait_result, trait_results))
    # else:
    #     with open(file, "r") as f:
    #         trait_results = json.load(f)

    if skip_timeouts:
        trait_results = filter(lambda x: "NO DATA (timed out)" not in x.values(), trait_results)

    return pd.DataFrame(trait_results).convert_dtypes()


def load_curves(source: str) -> pd.DataFrame:
    def project(record: Dict[str, Any]):
        projection = {}
        projection["curve"] = record["name"]
        projection["standard"] = record["standard"]
        projection["bitlength"] = int(record["field"]["bits"])
        projection["field"] = record["field"]["type"]
        projection["cofactor"] = (
            int(record["cofactor"], base=16)
            if isinstance(record["cofactor"], str)
            else int(record["cofactor"])
        )
        return projection

    if source.startswith("mongodb"):
        curve_records = database.get_curves(database.connect(source), dict(), raw=True)
    else:  # source.startswith("http"):
        with urllib.request.urlopen(source + "dissect.curves.json.bz2") as f:
            curve_records = json.loads(bz2.decompress(f.read()).decode("utf-8"))
    # else:
    #     with open(file, "r") as f:
    #         curve_records = json.load(f)

    df = pd.DataFrame(map(project, curve_records)).convert_dtypes()
    return df


def get_trait_df(source: str, curves, trait_name):
    # load all results for the given trait
    df_trait = load_trait(source, trait_name)
    # join curve metadata to trait results
    df_trait = curves.merge(df_trait, "right", "curve")
    return df_trait


def filter_choices(choices, ignored):
    filtered = {}
    for key in choices:
        if key not in ignored:
            filtered[key] = choices[key]
    return filtered


def get_params(choices):
    return filter_choices(
        choices, ["source", "bitlength", "field", "cofactor", "Feature:", "Modifier:"]
    )


def filter_df(df, choices):
    # TODO this way of checking is expensive - add curve categories to DB
    allowed_curves = []
    for source in choices["source"]:
        allowed_curves += STD_CURVE_DICT.get(source, [])

    if "sim" not in choices["source"]:
        df = df[df.standard == True]

    if "std" not in choices["source"]:
        df = df[df.curve.isin(allowed_curves) | (df.standard == False)]

    df = df[df.field.isin(choices["field"])]
    filtered = filter_choices(choices, ["source", "field", "Feature:", "Modifier:"])

    for key, value in filtered.items():
        options = list(map(int, value))
        df = df[df[key].isin(options)]

    return df


def get_all(df, choices):
    modifier = getattr(Modifier, choices["Modifier:"])()
    feature = choices["Feature:"]
    params = get_params(choices)
    if len(params) == 0:
        return [(filter_df(df, choices), params, feature, modifier, choices["Modifier:"])]
    param, values = params.popitem()
    choices.pop(param)
    results = []
    for v in values:
        param_choice = choices.copy()
        param_choice[param] = [v]
        results.append((filter_df(df, param_choice), param_choice, feature, modifier, choices["Modifier:"]))
    return results


def find_outliers(df, features):
    df = df.copy(deep=True)
    mms = MinMaxScaler()
    df[features] = mms.fit_transform(df[features].values)
    lof = LocalOutlierFactor()
    data = df[features]
    lof.fit(data)
    predictions = lof.fit_predict(data)
    return df[predictions == -1]


def flatten_trait(trait_name, trait_df):
    result_df = trait_df[["curve"]].drop_duplicates(subset=["curve"])

    for params in params_iter(trait_name):
        if params:
            for param in params:
                param_df = trait_df[trait_df[param] == params[param]]

            param_df = param_df.drop(params.keys(), axis=1)
        else:
            param_df = trait_df

        param_df = param_df.drop(nonnumeric_outputs(trait_name), axis=1)
        param_df.columns = map(lambda x: "curve" if x == "curve" else f"{x}_{params}", param_df.columns)
        result_df = result_df.merge(param_df, "left", on="curve")

    return result_df
