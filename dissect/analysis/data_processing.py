from typing import Dict, Any
from decimal import Decimal
import urllib.request
import json
import bz2

import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import KMeans

import dissect.utils.database_handler as database
from dissect.traits import TRAITS


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

    return pd.DataFrame(map(project, curves))


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
        trait_results = filter(lambda x: "NO DATA" not in x.values(), trait_results)
        trait_results = filter(lambda x: "NO DATA (timed out)" not in x.values(), trait_results)
        trait_results = filter(lambda x: "INVALID DATA Ran out of input" not in x.values(), trait_results)

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


def find_clusters(df, features, n_clusters=2):
    df = df.copy(deep=True)
    data = df[features]
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(data)
    return pd.DataFrame({
        "curve": df["curve"],
        "cluster": kmeans.labels_,
        "category": df["category"]
    })


def flatten_trait(trait_name, trait_df, param_values = None, ignore_curve_data = True):
    result_df = trait_df[["curve"]].drop_duplicates(subset=["curve"])

    for params in TRAITS[trait_name].params_iter():
        if param_values and not list(params.values())[0] in param_values:
            continue
        if params:
            for param in params:
                param_df = trait_df[trait_df[param] == params[param]]

            param_df = param_df.drop(params.keys(), axis=1, errors="ignore")
        else:
            param_df = trait_df

        param_df = param_df.drop(TRAITS[trait_name].nonnumeric_outputs(), axis=1, errors="ignore")
        if ignore_curve_data:
            param_df = param_df.drop(filter(lambda x: x in ("bits", "category", "cofactor", "field_type", "standard", "example"), param_df.columns), axis=1, errors="ignore")
        param_df.columns = map(lambda x: "curve" if x == "curve" else f"{trait_name}_{x}_{params}", param_df.columns)

        result_df = result_df.merge(param_df, "left", on="curve")

    return result_df


def clean_feature(df, feature):
    def cleaner(value):
        try:
            return Decimal(value)
        except:
            return pd.NA

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
