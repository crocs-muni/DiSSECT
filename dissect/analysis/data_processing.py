from typing import Dict, Any
import urllib.request
import json
import bz2
from sage.all import RR, ZZ

import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import MinMaxScaler

import dissect.utils.database_handler as database
from dissect.definitions import STD_CURVE_DICT, ALL_CURVE_COUNT, ALL_COFACTORS
from dissect.traits.trait_info import TRAIT_INFO, params_iter, nonnumeric_outputs


class Modifier:
    """a class of lambda functions for easier modifications if visualised values"""

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


def get_curves(source: str, query: Dict[str, Any] = {}):
    def project(record: Dict[str, Any]):
        projection = {}
        projection["curve"] = record["name"]
        projection["category"] = record["category"]
        projection["standard"] = record["standard"]
        projection["example"] = record["example"]
        projection["category"] = record["category"]
        projection["bitlength"] = int(record["field"]["bits"])
        projection["field"] = record["field"]["type"]
        projection["cofactor"] = (
            int(record["cofactor"], base=16)
            if isinstance(record["cofactor"], str)
            else int(record["cofactor"])
        )
        return projection

    curves = []
    if source.startswith("mongodb"):
        curves = database.get_curves(database.connect(source), query)
    elif source.startswith("http"):
        args = []
        for key in query:
            if isinstance(query[key], list):
                for item in query[key]:
                    args.append(f"{key}={item}")
            else:
                args.append(f"{key}={query[key]}")
        args = "&".join(args)

        req = urllib.request.Request(f"{source}db/curves?{args}", method="GET")

        with urllib.request.urlopen(req) as f:
            curves = json.loads(f.read())["data"]

    return pd.DataFrame(map(project, curves)).convert_dtypes()


def get_trait(source: str, trait_name: str, query: Dict[str, Any] = {}, skip_failed=True):
    trait_results = []
    if source.startswith("mongodb"):
        trait_results = database.get_trait_results(database.connect(source), trait_name, query)
    elif source.startswith("http"):
        args = []
        for key in query:
            if isinstance(query[key], list):
                for item in query[key]:
                    args.append(f"{key}={item}")
            else:
                args.append(f"{key}={query[key]}")
        args = "&".join(args)

        req = urllib.request.Request(f"{source}db/trait/{trait_name}?{args}", method="GET")

        with urllib.request.urlopen(req) as f:
            trait_results = json.loads(f.read())["data"]


    if skip_failed:
        trait_results = filter(lambda x: "NO DATA (timed out)" not in x.values(), trait_results)

    return pd.DataFrame(trait_results).convert_dtypes()


def get_curve_categories(source: str):
    if source.startswith("mongodb"):
        return list(database.get_curve_categories(database.connect(source)))
    if source.startswith("http"):
        req = urllib.request.Request(f"{source}db/curve_categories", method="GET")

        with urllib.request.urlopen(req) as f:
            return json.loads(f.read())["data"]


def filter_choices(choices, ignored):
    filtered = {}
    for key in choices:
        if key not in ignored:
            filtered[key] = choices[key]
    return filtered


def get_params(choices):
    return filter_choices(
        choices, ["category", "bits", "field_type", "cofactor", "Feature:", "Modifier:"]
    )


def filter_df(df, choices):
    # TODO this way of checking is expensive - add curve categories to DB
    df = df[df.field_type.isin(choices["field_type"])]
    filtered = filter_choices(choices, ["category", "field_type", "Feature:", "Modifier:"])

    for key, value in filtered.items():
        if "all" not in value:
            options = list(map(int, value))
            df = df[df[key].isin(options)]


    return df


def get_all(df, choices):
    modifier = getattr(Modifier, choices["Modifier:"])()
    feature = choices["Feature:"]
    params = get_params(choices)
    if len(params) == 0:
        return [[df, params, feature, modifier, choices["Modifier:"]]]
    param, values = params.popitem()
    choices.pop(param)
    results = []
    for v in values:
        param_choice = choices.copy()
        param_choice[param] = [v]
        results.append((df, param_choice, feature, modifier, choices["Modifier:"]))
    return results


def find_outliers(df, features):
    df = df.copy(deep=True)
    lof = LocalOutlierFactor()
    data = df[features]
    lof.fit(data)
    predictions = lof.fit_predict(data)
    return df[predictions == -1]


def flatten_trait(trait_name, trait_df, param_values = None, ignore_curve_data = True):
    result_df = trait_df[["curve"]].drop_duplicates(subset=["curve"])

    for params in params_iter(trait_name):
        if param_values and not list(params.values())[0] in param_values:
            continue
        if params:
            for param in params:
                param_df = trait_df[trait_df[param] == params[param]]

            param_df = param_df.drop(params.keys(), axis=1, errors="ignore")
        else:
            param_df = trait_df

        param_df = param_df.drop(nonnumeric_outputs(trait_name), axis=1, errors="ignore")
        if ignore_curve_data:
            param_df = param_df.drop(filter(lambda x: x in ("bits", "category", "cofactor", "field_type", "standard", "example"), param_df.columns), axis=1, errors="ignore")
        param_df.columns = map(lambda x: "curve" if x == "curve" else f"{trait_name}_{x}_{params}", param_df.columns)

        result_df = result_df.merge(param_df, "left", on="curve")

    return result_df
