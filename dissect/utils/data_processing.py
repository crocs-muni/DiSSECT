from typing import Dict, Any

import pandas as pd
from tqdm.contrib import tmap

from sage.all import RR, ZZ
import dissect.utils.database_handler as database
from dissect.definitions import STD_CURVE_DICT, ALL_CURVE_COUNT

db = None


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


def load_trait(
        trait: str, params: Dict[str, Any] = None, curve: str = None
) -> pd.DataFrame:
    global db
    if not db:
        db = database.connect()

    trait_results = database.get_trait_results(db, trait)
    return pd.DataFrame(trait_results).convert_dtypes()


def load_curves(filters: Any = {}) -> pd.DataFrame:
    global db
    if not db:
        db = database.connect()

    def project(record: Dict[str, Any]):
        projection = {}
        projection["curve"] = record["name"]
        projection["simulated"] = record["simulated"]
        projection["bitlength"] = int(record["field"]["bits"])
        projection["cofactor"] = (
            int(record["cofactor"], base=16)
            if isinstance(record["cofactor"], str)
            else int(record["cofactor"])
        )
        return projection

    curve_records = database.get_curves(db, filters, raw=True)
    df = pd.DataFrame(
        tmap(project, curve_records, desc="Loading curves", total=ALL_CURVE_COUNT)
    ).convert_dtypes()
    return df


def get_trait_df(curves, trait_name):
    # load all results for the given trait
    df_trait = load_trait(trait_name)
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
        choices, ["source", "bitlength", "cofactor", "Feature:", "Modifier:"]
    )


def filter_df(df, choices):
    # TODO this way of checking is expensive - add curve categories to DB
    allowed_curves = []
    for source in choices["source"]:
        allowed_curves += STD_CURVE_DICT.get(source, [])

    if "sim" not in choices["source"]:
        df = df[df.simulated == False]

    if "std" not in choices["source"]:
        df = df[df.curve.isin(allowed_curves) | (df.simulated == True)]

    filtered = filter_choices(choices, ["source", "Feature:", "Modifier:"])

    for key, value in filtered.items():
        options = list(map(int, value))
        df = df[df[key].isin(options)]

    return df


def get_all(df, choices):
    param, values = get_params(choices).popitem()
    choices.pop(param)
    for v in values:
        param_choice = choices.copy()
        param_choice[param] = [v]
        feature = choices["Feature:"]
        modifier = getattr(Modifier, choices["Modifier:"])()
        yield filter_df(df, param_choice), param_choice, feature, modifier
