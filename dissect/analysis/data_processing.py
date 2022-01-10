from typing import Dict, Any
import urllib.request
import json
import bz2

import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import MinMaxScaler

import dissect.utils.database_handler as database
from dissect.traits.trait_info import TRAIT_INFO, params_iter, nonnumeric_outputs


def get_curves(source: str, query: Dict[str, Any] = {}):
    def project(record: Dict[str, Any]):
        projection = {}
        projection["curve"] = record["name"]
        projection["category"] = record["category"]
        projection["standard"] = record["standard"]
        projection["example"] = record["example"]
        projection["category"] = record["category"]
        projection["bitlength"] = record["field"]["bits"]
        projection["field"] = record["field"]["type"]
        projection["cofactor"] = record["cofactor"]
        projection["order"] = record["order"]
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
